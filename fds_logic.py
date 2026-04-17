import pandas as pd
import re
import os

def process_fds_data(file_path, parameters_info_override=None, column_mapping=None):
    """
    Обробляє дані FDS, генерує графіки з критичними значеннями
    та повертає оброблені дані та інформацію про критичні точки для відображення.

    Args:
        file_path (str): Шлях до вхідного файлу FDS (.txt або .csv).
        parameters_info_override (dict, optional): Словник з інформацією про параметри,
                                                   що перекриває стандартні. За замовчуванням None.
        column_mapping (dict, optional): Словник маппінгу колонок: {назва_колонки: код_параметра}.
                                        Дозволяє вручну вказати відповідність колонок до параметрів.

    Returns:
        tuple: (df, critical_points_data, parameters_info, parameter_order, actual_column_map)
               df (pd.DataFrame): Оброблені дані.
               critical_points_data (dict): Словник з критичними точками для кожного параметра.
               parameters_info (dict): Актуальна інформація про параметри, що використовувалася.
               parameter_order (list): Порядок параметрів для сортування.
               actual_column_map (dict): Мапа (param_code, sensor_num) -> column_name.
    """
    try:
        # --- 1. Завантаження даних ---
        # pd.read_csv коректно читає як .txt, так і .csv файли.
        # header=[0, 1] - читає два рядки як заголовки
        # skipinitialspace=True - допомагає з пробілами після коми
        df = pd.read_csv(file_path, header=[0, 1], skipinitialspace=True)

        # --- 2. Парсинг заголовків та даних ---
        new_columns = []
        for unit_header, param_sensor_header in df.columns:
            cleaned_unit_header = unit_header.replace('"', '').replace("'", '')
            cleaned_param_sensor_header = param_sensor_header.replace('"', '').replace("'", '')

            # Заголовки FDS можуть бути трохи заплутаними.
            # Намагаємося створити зрозумілі назви колонок.
            if 'Unnamed' in param_sensor_header:
                # Це, ймовірно, перша колонка "Time" або "s" без підзаголовка
                new_columns.append(cleaned_unit_header)
            else:
                new_columns.append(f"{cleaned_param_sensor_header} ({cleaned_unit_header})")
        
        df.columns = new_columns
        
        # Перейменовуємо колонку часу на "Time" для зручності
        if 's' in df.columns:
            df.rename(columns={'s': 'Time'}, inplace=True)
        elif 'Time (s)' in df.columns:
            df.rename(columns={'Time (s)': 'Time'}, inplace=True)

        # Перевірка наявності колонки "Time"
        if 'Time' in df.columns:
            df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
        else:
            raise ValueError("Колонка 'Time' не знайдена після парсингу заголовків. Перевірте формат файлу.")

        # Перетворення всіх інших колонок на числові
        for col in df.columns:
            if col != 'Time':
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Видалення рядків, де всі значення, крім часу, є NaN (порожні)
        df.dropna(how='all', subset=[col for col in df.columns if col != 'Time'], inplace=True)

        # --- 3. Визначення параметрів та сенсорів ---
        # Якщо parameters_info_override надано (з GUI), використовуємо його.
        # Інакше використовуємо стандартний словник.
        if parameters_info_override:
            parameters_info = parameters_info_override
        else:
            parameters_info = {
                'Temp': {'name': 'Температура', 'unit': 'C', 'critical': 60.0, 'direction': 'above'}, 
                'Visio': {'name': 'Видимість', 'unit': 'm', 'critical': 20.0, 'direction': 'below'}, 
                'TP': {'name': 'Тепловий потік', 'unit': 'kW/m2', 'critical': 20.0, 'direction': 'above'},
                'KK': {'name': 'Кисень', 'unit': 'kg/m3', 'critical': 0.15, 'direction': 'below'}, 
                'OV': {'name': 'Оксид вуглецю', 'unit': 'kg/m3', 'critical': 0.015, 'direction': 'above'},
                'DV': {'name': 'Діоксид вуглецю', 'unit': 'kg/m3', 'critical': 0.05, 'direction': 'above'}
            }
        
        # Порядок параметрів для сортування (важливо для послідовного відображення)
        parameter_order = list(parameters_info.keys())


        # --- 4. Аналіз критичних значень та підготовка даних для графіків ---
        critical_points_data = {} 
        column_name_parser = re.compile(r'([A-Za-z]+)(\d+)\s*\((.*?)\)')

        # Формуємо мапу фактичних колонок DataFrame до їх кодів параметрів і номерів датчиків
        # OrderedDict зберігає порядок додавання елементів (порядок колонок у DataFrame)
        from collections import OrderedDict
        actual_column_map = OrderedDict()
        
        # Якщо є маппінг колонок (і він не порожній), використовуємо його
        if column_mapping and len(column_mapping) > 0:
            # Лічильник для генерації номерів сенсорів по кожному параметру
            param_sensor_counter = {}
            
            for col_name_in_df in df.columns:
                if col_name_in_df in column_mapping:
                    param_code = column_mapping[col_name_in_df]
                    if param_code in parameters_info:
                        # Спробуємо витягти номер сенсора з назви колонки
                        # Шукаємо числа в назві колонки (підтримуємо формати: "00", "01", "1", "2" тощо)
                        sensor_num = None
                        
                        # Пробуємо різні патерни для витягування номера
                        # Шукаємо числа після пробілу або в будь-якому місці назви
                        number_patterns = [
                            r'\s+(\d+)\s*\(',  # "Назва 01 (одиниця)" або "Назва 1 (одиниця)"
                            r'_(\d+)\s*\(',    # "Назва_01 (одиниця)"
                            r'(\d+)\s*\(',     # "Назва01 (одиниця)"
                            r'\s+(\d+)$',      # "Назва 01" в кінці
                            r'_(\d+)$',        # "Назва_01" в кінці
                            r'(\d+)$',         # "Назва01" в кінці
                        ]
                        
                        for pattern in number_patterns:
                            num_match = re.search(pattern, col_name_in_df)
                            if num_match:
                                sensor_num = int(num_match.group(1))
                                break
                        
                        # Якщо не знайшли номер, генеруємо автоматично
                        if sensor_num is None:
                            if param_code not in param_sensor_counter:
                                param_sensor_counter[param_code] = 1
                            else:
                                param_sensor_counter[param_code] += 1
                            sensor_num = param_sensor_counter[param_code]
                        
                        actual_column_map[(param_code, sensor_num)] = col_name_in_df
        else:
            # Стандартний підхід - парсинг назв колонок
            for col_name_in_df in df.columns:
                match = column_name_parser.match(col_name_in_df)
                if match:
                    param_code_from_col = match.group(1)
                    sensor_num_from_col = int(match.group(2))
                    unit_from_col = match.group(3)

                    # Перевіряємо, чи відомий цей код параметра і чи збігаються одиниці
                    if param_code_from_col in parameters_info and \
                       parameters_info[param_code_from_col]['unit'] == unit_from_col:
                        actual_column_map[(param_code_from_col, sensor_num_from_col)] = col_name_in_df
                elif col_name_in_df == 'Time':
                    continue # Пропускаємо колонку часу

        # Перебираємо всі виявлені параметри та датчики для аналізу критичних значень
        for (param_code, sensor_num), col_name_in_df in actual_column_map.items():
            info = parameters_info[param_code]
            critical_value = info['critical']
            direction = info['direction'] # Отримуємо напрямок (above/below)
            
            series = df[col_name_in_df]
            first_critical_occurrence = None 
            
            # Перевіряємо, чи є дані в серії та чи перше значення не є NaN
            if len(series) > 0 and pd.notna(series.iloc[0]):
                is_critical_at_start = False
                if direction == 'above':
                    is_critical_at_start = (series.iloc[0] > critical_value)
                elif direction == 'below':
                    is_critical_at_start = (series.iloc[0] < critical_value)

                if is_critical_at_start:
                    # Якщо значення вже є критичним на Time = 0, то це і є перший час досягнення
                    first_critical_occurrence = {'time': df['Time'].iloc[0], 'value': series.iloc[0]}
                else: 
                    # Якщо значення починається в безпечній зоні, шукаємо перше перетинання в критичну зону
                    for i in range(1, len(series)):
                        current_time = df['Time'].iloc[i]
                        current_value = series.iloc[i]
                        previous_value = series.iloc[i-1]
                        
                        # Перевіряємо, чи значення не є NaN
                        if pd.notna(current_value) and pd.notna(previous_value):
                            if direction == 'above':
                                # Перетин з (менше або дорівнює критичному) до (більше критичного)
                                if current_value > critical_value and previous_value <= critical_value:
                                    first_critical_occurrence = {'time': current_time, 'value': current_value}
                                    break
                            elif direction == 'below':
                                # Перетин з (більше або дорівнює критичному) до (менше критичного)
                                if current_value < critical_value and previous_value >= critical_value:
                                    first_critical_occurrence = {'time': current_time, 'value': current_value}
                                    break
            
            # Зберігаємо знайдену критичну точку
            if first_critical_occurrence:
                critical_points_data[f"{param_code}_{sensor_num}"] = [first_critical_occurrence]
            else:
                critical_points_data[f"{param_code}_{sensor_num}"] = []


        return df, critical_points_data, parameters_info, parameter_order, actual_column_map

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{file_path}' не знайдено. Перевірте шлях.")
    except Exception as e:
        # Для діагностики можна вивести більше деталей помилки
        import traceback
        traceback.print_exc()
        raise Exception(f"Виникла помилка під час обробки даних: {e}. Перевірте формат файлу.")
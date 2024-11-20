from datetime import datetime

from core.config import settings
from core.oauth_apisheets import (
    get_service,
    get_sheet_access,
    get_sheet_by_name
)
from core.utils import get_columnletter_alias

import pandas as pd

if __name__ == '__main__':
    
        
            
            service = get_service()
            print('servicio obtenido!')
            print('spreadsheet',settings.ID_SPREADSHEET)
            sheet = get_sheet_access(service, settings.ID_SPREADSHEET)
            print('leyendo hoja de excel')

            pages = [
                'Hotline',
                'Mail',
                'Webchat',
                'Whatsapp',
                'Tickets'
            ]

            gid_pages = {
                'Hotline': '0',
                'Mail': '146816959',
                'Webchat': '344883390',
                'Whatsapp': '422285232',
                'Tickets': '1795485021'
            }

            for page in pages:
                print(f'Leyendo página: {page}')
                sheet = get_sheet_by_name(service, settings.ID_SPREADSHEET, page)
                # Leer el archivo Excel
                main_file = pd.read_excel(io=settings.EXCEL_ROUTE, sheet_name=page)
                
                # Obtener encabezados y datos
                headers = main_file.columns.tolist()
                print(headers)
                data = main_file.astype(str).values.tolist()

                # Determinar tamaño de las columnas y filas
                col_size = len(headers)
                alias_col = get_columnletter_alias(col_size)
                row_size = len(data)
                
                # Definir la fila de inicio para los resultados
                index_results = 2
                tot_results = row_size + index_results
                
                # Definir rango para los datos a insertar (en formato texto)
                range_results = 'A{}:{}{}'.format(
                    index_results,
                    alias_col,
                    tot_results
                )

                # Definir rango para los encabezados
                header_range = 'A1:{}1'.format(
                    alias_col
                )

                # Actualización de los encabezados
                sheet.batch_update([{
                    'range': header_range,
                    'values': [headers],
                }], value_input_option='USER_ENTERED')

                # Actualización de los datos
                sheet.batch_update([{
                    'range': range_results,
                    'values': data,
                }], value_input_option='USER_ENTERED')
                
                print(f'\n\nLa página {page} fue actualizada exitosamente')

        
           
            
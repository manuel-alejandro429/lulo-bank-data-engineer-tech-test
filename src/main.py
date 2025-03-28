from flask import abort
from types import SimpleNamespace
import logging

# logging para visualización de mensajes/logs en producción
logging.basicConfig(level=logging.INFO)


def start(request: SimpleNamespace):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '60'
        }
        return '', 204, headers

    elif request.method == 'POST':
        logging.info("Iniciando proceso de extracción de datos desde API...")

        #
        #
        #
        #

        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*'
        }

        return 'Extracción completada exitosamente.', 200, headers

    else:
        return abort(405)


if __name__ == '__main__':
    start(SimpleNamespace(method='POST'))
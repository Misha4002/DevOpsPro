import psycopg2
from flask import Flask, request, jsonify
import datetime

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        operation = data['operation']
        operand1 = float(data['operand1'])
        operand2 = float(data['operand2'])

        if operation == 'add':
            result = operand1 + operand2
        elif operation == 'subtract':
            result = operand1 - operand2
        elif operation == 'multiply':
            result = operand1 * operand2
        elif operation == 'divide':
            if operand2 == 0:
                return jsonify({'error': 'Division by zero is not allowed'}), 400
            result = operand1 / operand2
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        log_calculation(operation, operand1, operand2, result)
        return jsonify({'result': result})

    except (KeyError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def log_calculation(operation, operand1, operand2, result):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="calculator_db",  # Use the new 'calculator_db'
            user="mishalapko",
            password=""  # Add your password if required
        )
        cursor = conn.cursor()

        query = """
        INSERT INTO calculation_logs (operation, operand1, operand2, result)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (operation, operand1, operand2, result))
        conn.commit()

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error logging calculation: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5552)

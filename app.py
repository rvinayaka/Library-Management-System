from flask import Flask, request, jsonify
from conn import connection
from settings import logger, handle_exceptions
import psycopg2

app = Flask(__name__)
# Library management system - Design a class to manage library resources,
# including books, journals, and magazines, borrowing, and returning books.


# Table
#  sno |     type     | borrowed_on | returned | username
# -----+--------------+-------------+----------+----------
#    1 | Journal      | 2023-03-21  | t        | Anjali
#    2 | Magazine     | 2022-09-12  | f        | Kabir
#    3 | Encyclopedia | 1990-12-23  | t        | Kabir





@app.route('/register', methods=["GET", "POST"])
@handle_exceptions
def add_member():           # adding new people who have taken the things from library
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display items in the cart")

    book_type = request.json["type"]
    borrowed_on = request.json["borrowDate"]
    returned = request.json["returned"]
    username = request.json["username"]

    # format = {
    #     "type": "Magazine",
    #     "borrowDate": "2022-09-12",
    #     "returned": "False",
    #     "username": "Anya"
    # }

    print(type, borrowed_on, returned)

    add_query = """INSERT INTO library(type, username, 
                                    borrowed_on, returned) VALUES (%s, %s, %s, %s)"""
    values = (book_type, username, borrowed_on, returned)
    cur.execute(add_query, values)

    # commit to database
    conn.commit()
    logger(__name__).info(f"{username} added in the list")
    return jsonify({"message": f"{username} added in the list"}), 200


@app.route("/", methods=["GET"], endpoint='show_entries')            # READ the cart list
@handle_exceptions
def show_entries():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display members in the list")

    show_query = "SELECT * FROM library;"
    cur.execute(show_query)
    data = cur.fetchall()

    # Log the details into logger file
    logger(__name__).info("Displayed list of all member in the list")
    return jsonify({"message": data}), 200

@app.route("/library/<int:sno>", methods=["PUT"], endpoint='update_details')   # update the values of member
@handle_exceptions
def update_details(sno):
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    cur.execute("SELECT type from library where sno = %s", (sno,))
    get_character = cur.fetchone()

    if not get_character:
        return jsonify({"message": "Character not found"}), 200
    data = request.get_json()
    type = data.get('type')
    borrowed_on = data.get('borrowedOn')
    returned = data.get('returned')
    username = data.get('username')

    if type:
        cur.execute("UPDATE library SET type = %s WHERE sno = %s", (type, sno))
    if username:
        cur.execute("UPDATE library SET username = %s WHERE sno = %s", (username, sno))
    elif borrowed_on:
        cur.execute("UPDATE library SET borrowed_on = %s WHERE sno = %s", (borrowed_on, sno))
    elif returned:
        cur.execute("UPDATE library SET returned = %s WHERE sno = %s", (returned, sno))

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Member details updated: {data}")
    return jsonify({"message": "Member details updated", "Details": data}), 200

@app.route("/search/<string:username>", methods=["GET"], endpoint='search_by_username')
@handle_exceptions
def search_by_username(username):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to search user in the list")

    show_query = "SELECT * FROM library WHERE username = %s;"
    cur.execute(show_query, (username,))
    data = cur.fetchone()

    print(data)
    # Log the details into logger file
    logger(__name__).info("Displayed details of the member in the list")

    return jsonify({"message": data}), 200


@app.route("/history/<string:type>", methods=["GET"], endpoint='borrow_history')
@handle_exceptions
def borrow_history(type):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display borrow history in the list")

    show_query = "SELECT COUNT(*) AS borrow_Count FROM library WHERE type = %s;"
    cur.execute(show_query, (type,))
    data = cur.fetchone()

    print(data)
    # Log the details into logger file
    logger(__name__).info("Displayed details of the book type in the list")

    return jsonify({"message": data}), 200


@app.route("/report/<string:type>", methods=["GET"], endpoint='generate_report')
@handle_exceptions
def generate_report(type):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to generate report of books in the list")

    show_query = "SELECT * FROM library WHERE type = %s;"
    cur.execute(show_query, (type,))
    data = cur.fetchone()

    print(data)
    # Log the details into logger file
    logger(__name__).info("Generate report of book type in the list")

    return jsonify({"message": data}), 200



@app.route("/delete/<int:sno>", methods=["DELETE"], endpoint='delete_member')      # DELETE an item from cart
@handle_exceptions
def delete_member(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to delete member from the list")

    delete_query = "DELETE from library WHERE sno = %s"
    cur.execute(delete_query, (sno,))

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Account no {sno} deleted from the table")
    return jsonify({"message": "Deleted Successfully", "item_no": sno}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
from conn import connection
from settings import logger

app = Flask(__name__)
# Library management system - Design a class to manage library resources,
# including books, journals, and magazines, borrowing, and returning books.



#  sno |   type   | borrowed_on | returned
# -----+----------+-------------+----------
#    1 | Journal  | 2023-03-21  | t
#    2 | Magazine | 2022-09-12  | f

# New Features:
# Searching
# Book borrowing history
# generate

@app.route('/register', methods=["GET", "POST"])
def add_member():           # adding new people who have taken the things from library
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display items in the cart")

    try:
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
    except Exception as error:
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence member added, closing the connection")


@app.route("/", methods=["GET"])            # READ the cart list
def show_entries():
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display members in the list")

    try:
        show_query = "SELECT * FROM library;"
        cur.execute(show_query)
        data = cur.fetchall()

        # Log the details into logger file
        logger(__name__).info("Displayed list of all member in the list")
        return jsonify({"message": data}), 200
    except Exception as error:
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence members displayed, closing the connection")

@app.route("/library/<int:sno>", methods=["PUT"])   # update the values of member
def update_details(sno):
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to update the details ")

    try:
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
    except Exception as error:
        # Raise an error and log into the log file
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence member details updated, closing the connection")


@app.route("/search/<string:username>", methods=["GET"])
def search_by_username(username):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to search user in the list")

    try:
        show_query = "SELECT * FROM library WHERE username = %s;"
        cur.execute(show_query, (username, ))
        data = cur.fetchone()

        print(data)
        # Log the details into logger file
        logger(__name__).info("Displayed details of the member in the list")

        return jsonify({"message": data}), 200
    except Exception as error:
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence user searching done, closing the connection")


@app.route("/history/<string:type>", methods=["GET"])
def borrow_history(type):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display borrow history in the list")

    try:
        show_query = "SELECT COUNT(*) AS borrow_Count FROM library WHERE type = %s;"
        cur.execute(show_query, (type, ))
        data = cur.fetchone()

        print(data)
        # Log the details into logger file
        logger(__name__).info("Displayed details of the book type in the list")

        return jsonify({"message": data}), 200
    except Exception as error:
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence borrowed history displayed, closing the connection")


@app.route("/report/<string:type>", methods=["GET"])
def generate_report(type):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to generate report of books in the list")

    try:
        show_query = "SELECT * FROM library WHERE type = %s;"
        cur.execute(show_query, (type, ))
        data = cur.fetchone()

        print(data)
        # Log the details into logger file
        logger(__name__).info("Generate report of book type in the list")

        return jsonify({"message": data}), 200
    except Exception as error:
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence report has been generated, closing the connection")



@app.route("/delete/<int:sno>", methods=["DELETE"])      # DELETE an item from cart
def delete_member(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to delete member from the list")

    try:
        delete_query = "DELETE from library WHERE sno = %s"
        cur.execute(delete_query, (sno,))

        conn.commit()
        # Log the details into logger file
        logger(__name__).info(f"Account no {sno} deleted from the table")
        return jsonify({"message": "Deleted Successfully", "item_no": sno}), 200
    except Exception as error:
        logger(__name__).exception(f"Error occurred: {error}")
        return jsonify({"message": error})
    finally:
        # close the database connection
        conn.close()
        cur.close()
        logger(__name__).warning("Hence accounts deleted, closing the connection")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

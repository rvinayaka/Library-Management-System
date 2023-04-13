from flask import Flask, request, jsonify
from conn import connection
from settings import logger, handle_exceptions
import psycopg2

app = Flask(__name__)
# Library management system - Design a class to manage library resources,
# including books, journals, and magazines, borrowing, and returning books.


# Table
#  sno |  book_name   | borrowed_on | returned | username |      reviews      |   requests    | fine
# -----+--------------+-------------+----------+----------+-------------------+---------------+------
#    2 | Magazine     | 2022-09-12  | f        | Kabir    |                   |               |  200
#    3 | Encyclopedia | 1990-12-23  | t        | Kabir    | Perfectly written |               |    0
#    1 | Mein campf   | 2023-03-21  | t        | Anjali   | Nice novel        | Wings of Fire |    0




@app.route('/register', methods=["GET", "POST"])
@handle_exceptions
def add_member():           # adding new people who have taken the things from library
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display items in the cart")

    book_name = request.json["bookName"]
    borrowed_on = request.json["borrowDate"]
    returned = request.json["returned"]
    username = request.json["username"]

    # format = {
    #     "type": "Magazine",
    #     "borrowDate": "2022-09-12",
    #     "returned": "False",
    #     "username": "Anya"
    # }

    print(book_name, borrowed_on, returned)

    add_query = """INSERT INTO library(book_name, username, 
                                    borrowed_on, returned) VALUES (%s, %s, %s, %s)"""
    values = (book_name, username, borrowed_on, returned)
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

    cur.execute("SELECT username from library where sno = %s", (sno,))
    get_member = cur.fetchone()

    get_username = get_member[0]
    print(get_username)

    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    data = request.get_json()
    book_name = data.get('bookName')
    borrowed_on = data.get('borrowedOn')
    returned = data.get('returned')
    username = data.get('username')
    reviews = data.get('reviews')

    if book_name:
        cur.execute("UPDATE library SET book_name = %s WHERE sno = %s", (book_name, sno))
    if username:
        cur.execute("UPDATE library SET username = %s WHERE sno = %s", (username, sno))
    elif borrowed_on:
        cur.execute("UPDATE library SET borrowed_on = %s WHERE sno = %s", (borrowed_on, sno))
    elif returned:
        cur.execute("UPDATE library SET returned = %s WHERE sno = %s", (returned, sno))
    elif reviews:
        cur.execute("UPDATE library SET reviews = %s WHERE sno = %s", (reviews, sno))

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Details of {get_username} has been updated to {data}")
    return jsonify({"message": f"Details of {get_username} has been updated to {data}",
                    "Details": data}), 200

@app.route("/search/<string:username>", methods=["GET"], endpoint='search_by_username')
@handle_exceptions
def search_by_username(username):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to search user in the list")

    cur.execute("SELECT * from library where username = %s", (username,))
    get_member = cur.fetchone()

    get_username = get_member[0]
    print(get_username)

    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    show_query = "SELECT * FROM library WHERE username = %s;"
    cur.execute(show_query, (username,))
    data = cur.fetchone()

    print(data)
    # Log the details into logger file
    logger(__name__).info("Displayed details of the member in the list")

    return jsonify({"message": data}), 200


@app.route("/history/<string:book_name>", methods=["GET"], endpoint='borrow_history')
@handle_exceptions
def borrow_history(book_name):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to display borrow history in the list")

    show_query = "SELECT COUNT(*) AS borrow_Count FROM library WHERE book_name = %s;"
    cur.execute(show_query, (book_name,))
    data = cur.fetchone()
    data = data[0]

    print(data)
    # Log the details into logger file
    logger(__name__).info(f"{book_name} has been taken {data} number of times as shown in the list")

    return jsonify({"message": f"{book_name} has been taken {data} number of times as shown in the list"}), 200


@app.route("/report/<string:book_name>", methods=["GET"], endpoint='generate_report')
@handle_exceptions
def generate_report(book_name):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to generate report of books in the list")

    cur.execute("SELECT username from library where book_name = %s", (book_name,))
    get_member = cur.fetchone()

    get_username = get_member[0]
    print(get_username)

    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    show_query = "SELECT * FROM library WHERE book_name = %s;"
    cur.execute(show_query, (book_name,))
    data = cur.fetchone()

    report = data[0]
    print(data, report)
    # Log the details into logger file
    logger(__name__).info(f"Report of {book_name} generated in the list")

    return jsonify({"message": data}), 200



@app.route("/delete/<int:sno>", methods=["DELETE"], endpoint='delete_member')      # DELETE an item from cart
@handle_exceptions
def delete_member(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to delete member from the list")

    cur.execute("SELECT username from library where sno = %s", (sno,))
    get_member = cur.fetchone()

    get_username = get_member[0]
    print(get_username)

    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    delete_query = "DELETE from library WHERE sno = %s"
    cur.execute(delete_query, (sno,))

    conn.commit()
    # Log the details into logger file
    logger(__name__).info(f"Account no {sno} deleted from the table")
    return jsonify({"message": "Deleted Successfully", "item_no": sno}), 200

@app.route("/reviews/<int:sno>", methods=["PUT"], endpoint='add_reviews')
@handle_exceptions
def add_reviews(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to add reviews of book in the list")

    # Check if the member is in the list or not
    cur.execute("SELECT username, returned FROM library WHERE sno = %s", (sno,))
    get_member = cur.fetchone()

    # if member not available return not found
    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    get_username = get_member[0]                # username
    get_return_status = get_member[1]           # if return is TRUE or FALSE
    print(get_member, get_username, get_return_status)


    if get_return_status:
        # Get reviews from the member
        data = request.get_json()
        reviews = data.get('reviews')

        query = "UPDATE library SET reviews = %s WHERE sno = %s"
        values = (reviews, sno)

        # Execute the query
        cur.execute(query, values)

        # Commit the changes in the table
        conn.commit()

        # Log the details into logger file
        logger(__name__).info(f"{get_username} has been posted a review as {reviews}")

        return jsonify({"message": f"{get_username} has been posted a review as {reviews}"}), 200

    else:
        # Log the details into logger file
        logger(__name__).info(f"As {get_username} has not returned the book so can't post reviews")

        return jsonify({"message": f"As {get_username} has not returned the book so can't post reviews"}), 200


@app.route("/requests/<int:sno>", methods=["PUT"], endpoint='user_requests')
@handle_exceptions
def user_requests(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to add user's request in the list")

    # Check if the member is in the list or not
    cur.execute("SELECT username, returned FROM library WHERE sno = %s", (sno,))
    get_member = cur.fetchone()

    # if member not available return not found
    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    get_username = get_member[0]                # username
    get_return_status = get_member[1]           # if return is TRUE or FALSE
    print(get_member, get_username, get_return_status)


    if get_return_status:
        # Get all requests from the member
        data = request.get_json()
        requests = data.get('requests')

        query = "UPDATE library SET requests = %s WHERE sno = %s"
        values = (requests, sno)

        # Execute the query
        cur.execute(query, values)

        # Commit the changes in the table
        conn.commit()

        # Log the details into logger file
        logger(__name__).info(f"{get_username} has been posted request of {requests}")

        return jsonify({"message": f"{get_username} has been posted request of {requests}"}), 200

    else:
        # Log the details into logger file
        logger(__name__).info(f"As {get_username} has not returned the book so can't request")

        return jsonify({"message": f"As {get_username} has not returned the book so can't request"}), 200


@app.route("/fine_calc/<int:sno>", methods=["PUT"], endpoint='fine_calculations')
@handle_exceptions
def fine_calculations(sno):
    # start the database connection
    cur, conn = connection()
    logger(__name__).warning("Starting the db connection to calculate the user's fine if not returned")

    # Check if the member is in the list or not
    cur.execute("SELECT username, returned FROM library WHERE sno = %s", (sno,))
    get_member = cur.fetchone()

    # if member not available return not found
    if not get_member:
        return jsonify({"message": "Member not found"}), 200

    get_username = get_member[0]                # username
    get_return_status = get_member[1]           # if return is TRUE or FALSE
    print(get_member, get_username, get_return_status)


    if get_return_status:
        fine = 0

        query = "UPDATE library SET fine = %s WHERE sno = %s"
        values = (fine, sno)

        # Execute the query
        cur.execute(query, values)

        # Commit the changes in the table
        conn.commit()
        return jsonify({"message": f"{get_username} has returned the book, so no fine is applicable"})
    else:
        # Get borrowed date from the table
        cur.execute("SELECT borrowed_on FROM library WHERE sno = %s", (sno,))
        get_borrow_date = cur.fetchone()

        borrow_date = get_borrow_date[0]

        fine = request.json.get('fine')

        query = "UPDATE library SET fine = %s WHERE sno = %s"
        values = (fine, sno)

        # Execute the query
        cur.execute(query, values)

        # Commit the changes in the table
        conn.commit()

        # Log the details into logger file
        logger(__name__).info(f"{get_username} has borrowed book on {borrow_date} and not yet returned it, so the fine is {fine}")

        return jsonify({"message": f"{get_username} has borrowed book on {borrow_date} "
                                   f"and not yet returned it, so the fine is {fine}"}), 200




if __name__ == "__main__":
    app.run(debug=True, port=5000)

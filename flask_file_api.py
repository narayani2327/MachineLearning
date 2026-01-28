from flask import Flask, request

app = Flask(__name__)

@app.route("/loan")
def loan_details():
    loan_id = request.args.get("Loan_ID")
    income = request.args.get("ApplicantIncome")
    loan_amount = request.args.get("LoanAmount")

    return f"""
    <h2>Loan Details</h2>
    <p>Loan ID: {loan_id}</p>
    <p>Applicant Income: {income}</p>
    <p>Loan Amount: {loan_amount}</p>
    """

if __name__ == "__main__":
    app.run(debug=True)

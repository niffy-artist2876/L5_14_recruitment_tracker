"""Applicant tracking system for an HR team.

Stores applicants in SQLite, shortlists them against a salary budget,
updates their hiring status and exports a report.
"""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, "
    "role TEXT, expected_salary INTEGER, status TEXT)"
)


def add_applicant(name, role, expected_salary, status="applied"):
    """inserts a new applicant into the database"""
    conn.execute(
        "INSERT INTO applicants (name, role, expected_salary, status) "
        "VALUES (?, ?, ?, ?)",
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(role, salary_limit):
    """returns names of applicants for a role within the salary limit"""
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants WHERE role = ?",
        (role,),
    ).fetchall()
    result = []
    for name, salary in rows:
        if salary <= salary_limit:
            result.append(name)
    return result


def update_status(applicant_id, status):
    """changes an applicant's hiring status"""
    try:
        conn.execute("UPDATE applicants SET status = ? "
                     "WHERE id = ?", (status, applicant_id))
        conn.commit()
    except sqlite3.Error as err:
        print(f"Could not update applicant {applicant_id}: {err}")


def export_report(path):
    """writes each applicant's name, role and status to a CSV file"""
    with open(path, "w", encoding="utf-8") as report_file:
        for row in conn.execute("SELECT name, role, status FROM applicants"):
            report_file.write(",".join(row) + "\n")


def count_by_status(status):
    """returns how many applicants have the given status"""
    return conn.execute("SELECT COUNT(*) FROM applicants "
                        "WHERE status = ?", (status,)).fetchone()[0]


def main():
    """runs the app"""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)
    update_status(1, "interview")
    print(shortlist("analyst", 500000 + 150000))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()

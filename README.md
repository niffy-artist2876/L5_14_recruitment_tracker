# Lab 5: Static Code Analysis — Applicant Tracking System

**Your file:** `recruitment_tracker.py`

Follow the lab handout for the full instructions.

## About the program

A hiring tracker for an HR team. It stores job applicants in an SQLite database, shortlists candidates for a role against a salary budget, updates their hiring status and exports a report.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:
   ```bash
   python recruitment_tracker.py
   ```
   It runs a short demonstration and may create a small output file in the current folder, so run it from a folder you don't mind adding files to.

2. **Install the tools:**
   ```bash
   pip install pylint bandit flake8
   ```

3. **Run the analysis** and save the reports:
   ```bash
   pylint recruitment_tracker.py > pylint_report.txt
   bandit -r recruitment_tracker.py > bandit_report.txt
   flake8 recruitment_tracker.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | B608 | Security (Medium) | 8 | `addApplicant` builds the INSERT with an f-string, so a name like `O'Brien'); DROP TABLE...` gets run as SQL code. | Use a parametrized query like `VALUES (?, ?, ?, ?)` with a tuple of thevalues. |
   | B307 / W0123 | Security (Medium) | 14 | `eval(salary_rule)` runs any Python string passed in, so arbitrary code can be executed. | Pass the limit as an `int` , or use `ast.literal_eval` if it is required that it must be a string. |
   | B110 / W0718 | Security (Low) | 28–29 | `except Exception: pass` does nothing for every error, so a failed status update goes unnoticed. | Catch `sqlite3.Error` and re-raise it instead of `pass`. |
   | R1710 | Bug | 12–21 | `shortlist` returns a list when there are matches but `None` when there are no matches. | Always `return result`, which returns an empty list when nothing matches. |
   | R1732 / W1514 | Code quality | 32–35 | The file is opened without `with` or an `encoding`, so it isn't closed if a write fails. | `with open(path, "w", encoding="utf-8") as f:` (the `csv` module is better still). |
   | F841 / W0612 | Code quality | 15 | `total_seen` is assigned but never used. | Delete the line. |
   | C0103 | Style | 7, 24, 31, 32, 38 | Function names are camelCase (`addApplicant`, `updateStatus`, `exportReport`, `countByStatus`) instead of snake_case. Rename each function to its respective snake_case equivalent and update the calls in `main()`. |
   | E501 / C0301 | Style | 4, 8, 13, 26, 39 | Lines are too long. Flake8 (79-char limit) flags all five. Pylint flags lines 4, 8 and 13. | Split the SQL strings across multiple lines. |
   | C0114 / C0116 | Style | 1, 7, 12, 24, 31, 38, 42 | Missing module docstring and function docstrings. | Add one-line docstrings. |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

1. `recruitment_tracker.py`: your cleaned version, with at least 4 issues fixed.
2. `issues.md`: the completed issue table.
3. `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

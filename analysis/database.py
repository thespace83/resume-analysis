import mysql.connector

from analysis import Resume

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="profiggpro",
    database="resume-analysis"
)


def create_entry(resume: Resume):
    data = (
        resume.document_url,
        resume.name,
        resume.age,
        resume.gender,
        resume.education,
        resume.region,
        resume.profession,
        resume.experience,
        resume.type_of_employment,
        resume.info,
        resume.driving_license_category,
        resume.own_car,
        resume.citizenship
    )

    sql = """
    INSERT INTO resume
    (document_url, name, age, gender, education, region, profession, experience, type_of_employment, info, driving_license_category, own_car, citizenship) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor = cnx.cursor()
    try:
        cursor.execute(sql, data)
        cnx.commit()
    except mysql.connector.Error as e:
        cnx.rollback()
    finally:
        cursor.close()

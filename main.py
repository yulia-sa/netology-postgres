import psycopg2 as pg


student = {
    'name': "Дмитрий Петров",
    'gpa': 2.5,
    'birth': '1997-06-22'
}


students = [
    {
        'name': "Мария Иванова",
        'gpa': 4.7,
        'birth': '1994-04-04'
    },
    {
        'name': "Наталья Орлова",
        'gpa': 5.2,
        'birth': '1990-08-11'
    }
]


def create_db():  # создает таблицы
    with pg.connect("dbname=netology_db_homework") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE student (
                    id serial PRIMARY KEY,
                    name varchar(100),
                    gpa numeric(10,2),
                    birth timestamp with time zone);
                """)

            cur.execute("""
                CREATE TABLE course (
                    id serial PRIMARY KEY,
                    name varchar(100));
                """)

            cur.execute("""
                CREATE TABLE student_course (
                    id serial PRIMARY KEY,
                    student_id INTEGER REFERENCES student(id),
                    course_id INTEGER REFERENCES course(id));
                """)


def add_course(course):
    with pg.connect("dbname=netology_db_homework") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO course(name) VALUES (%s)
                """, (course, ))


def get_students(course_id):  # возвращает студентов определенного курса
    with pg.connect("dbname=netology_db_homework") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT s.name, s.gpa, s.birth FROM student s
                JOIN student_course sc
                ON s.id = sc.student_id
                WHERE sc.course_id = %s
                """, (course_id, ))
            student = cur.fetchall()
            return student


def add_students(course_id, students):  # создает студентов и
                                        # записывает их на курс
    conn = pg.connect("dbname=netology_db_homework")
    cur = conn.cursor()

    for i in range(0, len(students)):

        cur.execute("""
            INSERT INTO student(name, gpa, birth) VALUES (%s, %s, %s) RETURNING id
            """, (students[i]['name'], students[i]['gpa'], students[i]['birth']))

        added_student_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO student_course(student_id, course_id) VALUES (%s, %s)
            """, (added_student_id, course_id))

        conn.commit()


def add_student(student):  # просто создает студента
    with pg.connect("dbname=netology_db_homework") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO student(name, gpa, birth) VALUES (%s, %s, %s)
                """, (student['name'], student['gpa'], student['birth']))


def get_student(student_id):
    with pg.connect("dbname=netology_db_homework") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM student WHERE id = %s
                """, (student_id, ))
            student = cur.fetchone()
            return student


if __name__ == "__main__":
    create_db()
    add_course('Программирование на Python')
    add_course('Программирование на Javascript')
    add_course('Программирование на PHP')
    add_student(student)
    add_students(2, students)
    print(get_student(1))
    print(get_students(2))

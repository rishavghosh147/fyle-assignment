def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

def test_grade_assignment(client, h_teacher_1):
    response = client.post(
        '/teacher/assignments/grade',
        json={
            'id': 1,
            'grade': "B"
        },
        headers=h_teacher_1
    )

    print('*'*50,response.json)

    assert response.status_code == 200

    assert response.json['data']['state'] == "GRADED"
    assert response.json['data']['grade'] == "B"

def test_grade_assignment_regrade_error(client, h_teacher_1):
    """
    failure case: Assignment does not exist
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_None_value_error(client, h_teacher_1):
    """
    failure case: None value can't be acceptable
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": None,
            "grade": None
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'

def test_grade_assignment_Empty_value_error(client, h_teacher_1):
    """
    failure case: Empty value can't be acceptable
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": '',
            "grade": ''
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'
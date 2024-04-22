def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'


def test_post_assignment_empty_content(client, h_student_1):
    """
    failure case: content cannot be empty
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': ''
        })

    assert response.status_code == 400

def test_post_assignment_another_student(client, h_student_2):
    """
    failure case: Assignment belongs to another student
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'id':6,
            'content': 'this assignment is not mine'
        })

    assert response.status_code == 400

def test_post_assignment_not_exist(client, h_student_1):
    """
    failure case: Assignment does not exist
    """
    content = 'assignment not found'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id':0,
            'content': content
        })

    assert response.status_code == 404

def test_post_assignment_edited_successfully(client, h_student_1):
    content = 'try to edit an assignment'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id':6,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'

def test_post_submited_assignment_edit_error(client, h_student_1):
    """
    failure case: only assignment in draft state can be edited
    """
    content = 'try to edit an submited assignment'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id':2,
            'content': content
        })

    assert response.status_code == 400

    data = response.json
    assert data['message'] =='only assignment in draft state can be edited'

def test_post_assignment_with_None_id_teacher_id(client,h_student_1):
    """
    failure case: id and teacher_id can't be none
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': None,
            'teacher_id': None
        })

    assert response.status_code == 400

def test_post_assignment_with_Empty_id_teacher_id(client,h_student_1):
    """
    failure case: id and teacher_id can't be empty
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': '',
            'teacher_id': ''
        })

    assert response.status_code == 400


def test_assignment_not_exist_error(client, h_student_1):
    """
    failure case: Assignment does not exist
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 0,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'


def test_assignment_of_another_student(client, h_student_2):
    """
    failure case: This assignment belongs to some other student
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 6,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'This assignment belongs to some other student'


def test_Teacher_not_found(client, h_student_1):
    """
    failure case: Teacher does not exist
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 6,
            'teacher_id': 0
        })
    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Please enter a valid teacher id'

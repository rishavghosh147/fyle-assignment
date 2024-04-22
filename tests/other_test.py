def test_without_header(client):
    """
    failure case: header is missing
    """
    response =client.get(
        '/principal/teachers'
    )
    assert response.status_code==401
    data=response.json['message']
    assert data=='principal not found'

def test_get_all_teachers(client, h_principal):
    """
    failure case: when method is not get
    """
    response =client.post(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code==405

def test_app(client):
    response=client.get(
        '/'
    )
    value=response.json
    assert value['status']=='ready'
    assert response.status_code==200

def test_no_such_api(client):
    """
    failure case: api not found
    """
    response = client.get('/nonexistent_endpoint')
    assert response.status_code == 404

def test_try_authorize_principal_api_with_teacher_header(client, h_teacher_1):
    """
    failure case: when header is not belongs to principal
    """
    response =client.get(
        '/principal/teachers',
        headers=h_teacher_1
    )
    assert response.status_code==403
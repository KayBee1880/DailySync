def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Create Account" in response.data

def test_register_user(client, app):
    with app.app_context():
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'Password@123',
            'password2': 'Password@123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Login" in response.data
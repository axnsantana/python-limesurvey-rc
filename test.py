from pylimerc import PyLimeRc as RC

URL = "https://myurl.com/index.php/admin/remotecontrol"
SUVERY_ID = 123456
test = RC()
test.set_url("")
test.get_session_key("USERNAME", "PASSWORD")
test.add_participants(SUVERY_ID,
                      [{
                          "firstname": "A",
                          "lastname": "B",
                          "email": "XXX@gmail.com",
                          "emailstatus": "OK",
                          "language": "pl",
                          "token": "123456789"
                      }]
                      , True)

test.add_participants(SUVERY_ID,
                      [{
                          "firstname": "C",
                          "lastname": "D",
                          "email": "YYY@gmail.com",
                          "emailstatus": "OK",
                          "language": "pl",
                          "token": "123456789"
                      }]
                      , True)

test.invite_participants(SUVERY_ID)
print("OK")

import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBDX3x1g2d1qlAE0h81tOWkO6MV-gk-PYw",
  "authDomain": "covid-19-tracker-302dd.firebaseapp.com",
  "databaseURL": "https://covid-19-tracker-302dd.firebaseio.com",
  "projectId": "covid-19-tracker-302dd",
  "storageBucket": "covid-19-tracker-302dd.appspot.com",
  "messagingSenderId": "130878062861",
  "appId": "1:130878062861:web:2a478166f2463f25233044",
  "measurementId": "G-72XZ8TJ67W"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

# def upload_images():
#   path_on_cloud = "images/flags/india.png"
#   path_local = "images/flags/india.png"
#   storage.child(path_on_cloud).put(path_local)
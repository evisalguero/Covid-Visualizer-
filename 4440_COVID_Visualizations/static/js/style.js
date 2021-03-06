:root {
  --blue: #1e90ff;
  --white: #ffffff;
}

.alert-msg {
  color: red;
}

/* BASIC */

html {
  background-color: #56baed;
  margin: 0;
  height: 100%;
}

body {
  font-family: "Poppins", sans-serif;
  height: 100%;
  margin: 0;
}

a {
  color: #92badd;
  display:inline-block;
  text-decoration: none;
  font-weight: 400;
}

h2 {
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  display:inline-block;
}

/* STRUCTURE */

.content-wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 5vh;

  overflow: scroll;
}


/* LOGIN */

.login-wrapper {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 5vh;

  overflow: scroll;
}

.login-box {
  justify-content: space-around;
  width: 40%;
  height: 50vh;
  border-radius: 10px;

  color: var(--blue);
  background-color: var(--white);
  padding: 15px;
  box-shadow: 2px 2px 2px 2px #888888;
}

.login-title {
  color: var(--blue);
  font-size: 25px;
}

.login-form {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  padding: 5px;
}

.login-form-items {
  display: flex;
  flex-direction: column;
  margin: 20px;
}


/* HOME */

.page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.page-item {
  display: flex;
  justify-content: center;
  align-items: center;

  margin: 10px;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 2px 2px 2px 2px #888888;

  width: 90%;
  text-align: center;
}

.home-page-buttons {
  flex-wrap: wrap;
  justify-content: space-around;
}

.home-page-buttons a {
  margin: 10px;
}

.logout {
  position: relative;
  align-self: center;
}


/* OTHER */

.success-banner {
  position: absolute;
  top: 0px;
  height: 60px;
  width: 100%;
  padding: 20px 0;

  color: white;
  background-color: #38DF63;
  text-align: center;
}

.success-banner a {
  position: absolute;
  right: 20px;
  cursor: pointer;
}

const Instagram = require('instagram-web-api')
//const { username, password } = process.env

username = 'divasavum.troll';
password = 'hellothere!';
 
const client = new Instagram({username, password});
(async () => {
  let status = await client.login({ username: username, password: password }, { _sharedData: false })
  console.log(status);
  console.log('Inside this function!')
})()
const express = require('express')
const app = express()
const port = 3000
var gpiop = require('rpi-gpio').promise;

app.get('/', function (req, res) {
    gpiop.setup(11, gpiop.DIR_OUT)
    .then(() => {
        gpiop.write(11, false)
        timer(1000).then(_=>gpiop.write(11, true));
    })
    .catch((err) => {
        console.log('Error: ', err.toString())
    })
    res.send('Hello World!')
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))

const timer = ms => new Promise( res => setTimeout(res, ms));

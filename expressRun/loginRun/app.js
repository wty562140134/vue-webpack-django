var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

////////////////////////////////////////////////////////////////////////////////////////////
/*
HTTP前端服务器解决跨域
 */
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");//项目上线后改成页面的地址
    res.header("Access-Control-Allow-Headers", "X-Requested-With,Content-Type");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    next();
});

/*
HTTP前端服务器请求代理设置,这一段一定要放在处理404前面,不然会导致页面请求无法正常到达后端服务器
 */
var proxyMiddleWare = require('http-proxy-middleware');
var proxyOption = {
    target: 'http://127.0.0.1:8000',
    changeOrigoin: true,
    ws: true,
    pathRewrite: {
        '^/api': ''
    }
};
app.use(express.static(__dirname + "public"));
app.use("/api", proxyMiddleWare(proxyOption));
app.listen(4000);
////////////////////////////////////////////////////////////////////////////////////////////

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

module.exports = app;

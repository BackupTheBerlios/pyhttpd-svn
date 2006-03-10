<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<title>%(title)s - v%(version)s</title>
	<style type="text/css">
		input
		{
			border: 1px solid #000000;
		}
	</style>
</head>
<body>
	<div>
		<h3>%(title)s - v%(version)s</h3>
	</div>
	<div>
		<form action="/webadmin/login/" method="post">
			User:<br />
			<input type="text" name="user" />
			<br /><br />
			Password:<br />
			<input type="password" name="pass" />
			<br /><br />
			<input type="submit" value="Login!" />
		</form>
	</div>
</body>
</html>
from django.http import HttpResponse

def Home(request):
    return HttpResponse('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Endpoints</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
        }

        h2 {
            text-align: center;
            padding: 20px 0;
            color: #007bff;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th, td {
            padding: 10px;
            border-bottom: 2px solid #ddd;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
            font-weight: bold;
            color: #333;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        tr:hover {
            background-color: #f2f2f2;
        }

        code {
            background-color: #f9f9f9;
            padding: 2px 6px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h2>API Endpoints</h2>
    <table>
        <thead>
            <tr>
                <th>Endpoint</th>
                <th>Method</th>
                <th>Description</th>
                <th>Data</th>
                <th>Authorization Token</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><a href="/user/register">/user/register</a></td>
                <td><code>POST</code></td>
                <td>Register a new user.</td>
                <td>first_name, last_name, email, username, password</td>
                <td>No</td>
            </tr>
            <tr>
                <td><a href="/user/login">/user/login</a></td>
                <td><code>POST</code></td>
                <td>User login.</td>
                <td>username, password</td>
                <td>No</td>
            </tr>
            <tr>
                <td><a href="/user/">/user/</a></td>
                <td><code>GET</code></td>
                <td>Retrieve the user with the help of Token.</td>
                <td></td>
                <td>Yes</td>
            </tr>
            <tr>
                <td><a href="/user/">/user/</a></td>
                <td><code>PUT</code></td>
                <td>Update password of a user with the help of Token.</td>
                <td>password</td>
                <td>Yes</td>
            </tr>
            <tr>
                <td><a href="/user/">/user/</a></td>
                <td><code>DELETE</code></td>
                <td>Delete a user with the help of Token.</td>
                <td></td>
                <td>Yes</td>
            </tr>
            <tr>
                <td><a href="/blog/menu">/blog/menu</a></td>
                <td><code>GET</code></td>
                <td>Retrieve a list of available careers Data.</td>
                <td></td>
                <td>No</td>
            </tr>
            <tr>
                <td><a href="/blog/list">/blog/list</a></td>
                <td><code>GET</code></td>
                <td>Retrieve a list of all blogs of HomePage.</td>
                <td></td>
                <td>No</td>
            </tr>
            <tr>
                <td><a href="/blog/list">/blog/list</a></td>
                <td><code>POST</code></td>
                <td>Retrieve a list of all blogs of Particular career option.</td>
                <td>url</td>
                <td>No</td>
            </tr>
            <tr>
                <td><a href="/blog/content">/blog/content</a></td>
                <td><code>POST</code></td>
                <td>Retrieve content of a specific blog by URL.</td>
                <td>url</td>
                <td>No</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
''')
(() => {
    const fetchJson = async (url, options) => {
        try {
            return await fetchWithError(url,
                {
                    ...options,
                    headers: {
                        ...options.headers,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(options.body)
                })
        } catch (e) {
            console.log('Error has been occured in ' + url + " Return 'null' response by default.")
            return null
        }
    }

    const fetchWithError = async (url, options) => {
        url = 'http://127.0.0.1:8000/api/' + url
        const response = await fetch(url, options)
        if (response && !response.ok) {
            console.log('Error has been occurred in ' + url + ' . Status: ' + response.status)
        }
        return response
    }

    const registerUser = async (username) => {
        return await fetchJson('auth/users/',
            {
                method: 'POST',
                body: {
                    email: username + '@test.com',
                    password: '1234',
                    username: username,
                    sex: 'M'
                }
            })
    }

    const loginUser = async (username) => {
        const response = await fetchJson('auth/token/login/',
            {
                method: 'POST',
                body: {
                    'email': username + "@test.com",
                    'password': '1234'
                }
            })
        return response && (await response.json())['auth_token']
    }

    const removeUser = async (token) => {
        if (token) {
            return await fetchJson('auth/users/me/',
                {
                    method: 'DELETE',
                    headers: {
                        'Authorization': 'Token ' + token
                    },
                    body: {
                        'current_password': '1234'
                    }
                })
        }
    }
    const createSocket = async (username, token, url) => {
        return new Promise((resolve, reject) => {
            const socket = new WebSocket('ws://127.0.0.1:8000/ws/' + url)
            socket.onopen = () => {
                console.log(`[${username}.open]: Connection established`);
                socket.send(JSON.stringify({'type': 'auth', 'token': token}))
                resolve(socket)
            }
            socket.onmessage = (event) => {
                console.log(`[${username}.message]: ${event.data}.`);
            }
            socket.onclose = (event) => {
                if (event.wasClean) {
                    console.log(`[${username}.close] Clean close.`);
                } else {
                    console.log(`[${username}.close] Connection interrupted.`);
                }
            }
            socket.onerror = (error) => {
                console.log(`[${username}.error]: ${error.message}.`);
            }
            socket.onerror = error => reject(error);
        })
    }

    const printOnlineUsers = async (token) => {
        const onlineUsers = await fetchWithError('online/',
            {
                headers:
                    {
                        'Authorization': 'Token ' + token
                    }
            })
        console.log('online', await onlineUsers.json())
    }

    const getTokens = async (usernames) => {
        return await Promise.all(usernames.map(loginUser))
    }

    const testWebsockets = async (...usernames) => {
        await Promise.all((await getTokens(usernames)).map(removeUser))
        await Promise.all(usernames.map(registerUser))
        const tokens = await getTokens(usernames)
        const socket1 = await createSocket(usernames[0], tokens[0], 'blog/')
        await printOnlineUsers(tokens[0])
        const socket2 = await createSocket(usernames[0], tokens[0], 'blog/')
        await printOnlineUsers(tokens[1])
        await createSocket(usernames[1], tokens[1], 'blog/')
        await printOnlineUsers(tokens[1])
        await createSocket(usernames[2], tokens[2], 'blog/')
        const wrongSocket = await createSocket('wrongUser', 'wrongToken', 'blog/')
        await printOnlineUsers(tokens[1])
        socket2.close()
        await printOnlineUsers(tokens[1])
        const testData = JSON.stringify({
            'type': 'data',
            'targetUsername': 'user3',
            'comment': 'Some comment'
        })
        socket1.send(testData)
        const wrongData = JSON.stringify({
            'type': 'data',
            'comment': 'Some comment'
        })
        socket1.send(wrongData)
        wrongSocket.send(testData)
    }

    testWebsockets('user1', 'user2', 'user3')

})();


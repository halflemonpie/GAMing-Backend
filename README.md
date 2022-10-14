# GAMing-Backend

## About
This is the backend part for General Assembly Mentoring(GAMing), it mainly serves as the API to get data from the database. It has function to create, update, delete, and get user. It also allows the user to create their profiles and update them.

For all the endpoint for this API, please review `/api/docs'

## Create User
endpoint: http://localhost:8000/api/user/create/
method : POST

example request body:
{
  "email": "user9@example.com",
  "password": "test123",
  "full_name": "Test User8"
} 

successful response:
status code: 201
{
  "email": "user9@example.com",
  "full_name": "Test User8",
  "messages": [],
  "schedules": []
}

## Get User Token
endpoint: http://localhost:8000/api/user/token/
method: POST

example request body:
{
  "email": "user9@example.com",
  "password": "test123"
}

successful response:
status code: 200
{
  "token": "2c722a2ffdf50ba27f8f4ccf0be1a69d1a932636"
}

## Use token to login
Now we have the user token, we can use the token to create profile and update user. Please don't show this token to the user because they can use it to change profile and user setting.

## Create Profile
endpoint: http://localhost:8000/api/profile/profiles/
method: POST

add the token in the request header like this:
'Authorization: Token 2c722a2ffdf50ba27f8f4ccf0be1a69d1a932636'

example request body:
{
  "full_name": "Test User9",
  "short_description": "Hello, my name is User9. Nice to meet you",
  "description": "Hello, this is a example long description",
  "is_mentor": true,
  "skills": [
    {
      "name": "html"
    },
    {
      "name": "css"
    },
    {
      "name": "JavaScript"
    }
  ],
  "languages": [
    {
      "name": "English"
    }
  ]
}

example successful response:
status code: 201
{
  "id": 5,
  "user": 10,
  "full_name": "Test User9",
  "short_description": "Hello, my name is User9. Nice to meet you",
  "description": "Hello, this is a example long description",
  "is_mentor": true,
  "skills": [
    {
      "id": 9,
      "name": "html"
    },
    {
      "id": 10,
      "name": "css"
    },
    {
      "id": 11,
      "name": "JavaScript"
    }
  ],
  "languages": [
    {
      "id": 7,
      "name": "English"
    }
  ]
}

## Get User Profile
now we can use the get method to get the user profile list

endpoint: http://localhost:8000/api/profile/profiles/
method: GET

from now on we need to add the token to every request we make

example successful response:
status code: 200
	
[
  {
    "id": 5,
    "user": 10,
    "full_name": "Test User9",
    "short_description": "Hello, my name is User9. Nice to meet you",
    "description": "Hello, this is a example long description",
    "is_mentor": true,
    "skills": [
      {
        "id": 9,
        "name": "html"
      },
      {
        "id": 10,
        "name": "css"
      },
      {
        "id": 11,
        "name": "JavaScript"
      }
    ],
    "languages": [
      {
        "id": 7,
        "name": "English"
      }
    ]
  },
  {
    "id": 4,
    "user": 10,
    "full_name": "string",
    "short_description": "string",
    "description": "string",
    "is_mentor": true,
    "skills": [
      {
        "id": 8,
        "name": "string"
      }
    ],
    "languages": [
      {
        "id": 6,
        "name": "string"
      }
    ]
  },
  {
    "id": 3,
    "user": 3,
    "full_name": "user3",
    "short_description": "haha",
    "description": "new",
    "is_mentor": true,
    "skills": [
      {
        "id": 7,
        "name": "string"
      }
    ],
    "languages": [
      {
        "id": 5,
        "name": "string"
      }
    ]
  },
  {
    "id": 2,
    "user": 5,
    "full_name": "user2",
    "short_description": "user2's short description",
    "description": "long string",
    "is_mentor": false,
    "skills": [
      {
        "id": 3,
        "name": "html"
      },
      {
        "id": 4,
        "name": "css"
      },
      {
        "id": 5,
        "name": "JavaScript"
      }
    ],
    "languages": [
      {
        "id": 3,
        "name": "Spanish"
      }
    ]
  }
]

### Filter profile
we can filter the uer profile by adding parameter like this
endpoint: http://localhost:8000/api/profile/profiles/?languages=English&skills=html%2Ccss

example response:
status code: 200
[
  {
    "id": 5,
    "user": 10,
    "full_name": "Test User9",
    "short_description": "Hello, my name is User9. Nice to meet you",
    "description": "Hello, this is a example long description",
    "is_mentor": true,
    "skills": [
      {
        "id": 9,
        "name": "html"
      },
      {
        "id": 10,
        "name": "css"
      },
      {
        "id": 11,
        "name": "JavaScript"
      }
    ],
    "languages": [
      {
        "id": 7,
        "name": "English"
      }
    ]
  }
]

## Update user profile
we need to have the profile id for updating, in this case we have profile id of 5

endpoint: http://localhost:8000/api/profile/profiles/5/
method: PATCH

example request body(we only need to pass the information that we need to change):
{
  "full_name": "New Name",
  "is_mentor": false,
  "skills": [
    {
      "name": "UX Design"
    }
  ],
  "languages": [
    {
      "name": "English"
    }
  ]
}

example successful response:
status code: 200
{
  "id": 5,
  "user": 10,
  "full_name": "New Name",
  "short_description": "Hello, my name is User9. Nice to meet you",
  "description": "Hello, this is a example long description",
  "is_mentor": false,
  "skills": [
    {
      "id": 14,
      "name": "UX Design"
    }
  ],
  "languages": [
    {
      "id": 7,
      "name": "English"
    }
  ]
}

## Update user with new messages and Schedules
endpoint: http://localhost:8000/api/user/me/
method: PATCH

example request body:
{
  "password": "newpassword",
  "full_name": "new name",
  "messages": [
    {
      "type": "message",
      "sender": "user1",
      "receiver": "user9",
      "text": "Hello",
      "is_read": false
    }
  ],
  "schedules": [
    {
      "title": "Meeting with user1",
      "description": "Meet with other user",
      "start_time": "2022-10-14T20:51:10.123Z",
      "end_time": "2022-10-14T20:51:10.123Z",
      "participants": "user1, user2, user3"
    }
  ]
}

example successful response:
status code: 200
	
Response body
Download
{
  "email": "user9@example.com",
  "full_name": "new name",
  "messages": [
    {
      "id": 7,
      "type": "message",
      "sender": "user1",
      "receiver": "user9",
      "created_time": "2022-10-14T20:53:11.154332Z",
      "text": "Hello",
      "is_read": false
    }
  ],
  "schedules": [
    {
      "id": 2,
      "title": "Meeting with user1",
      "description": "Meet with other user",
      "start_time": "2022-10-14T20:51:10.123000Z",
      "end_time": "2022-10-14T20:51:10.123000Z",
      "participants": "user1, user2, user3"
    }
  ]
}
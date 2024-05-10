# VossieGram-Social media application

Welcome to my comprehensive social media platform, crafted with the powerful Django framework – a robust Python Web Framework. my platform offers a  user experience with real-time chatting capabilities, facilitated by Django and Channels utilizing websockets for instant communication.
Within our platform, users have the freedom to engage in a myriad of activities. They can effortlessly follow and unfollow other users, share their thoughts through posts, express appreciation by liking content, and explore diverse profiles. Our intuitive search feature allows users to easily discover others within the community.



## Installation Guide

Follow these steps to set up the project on your local machine:

note: to use the News-API you need to create an account "https://newsapi.org", then get your free api key. Create a config.py file in the main directory and write this line of code in the file and save the file:
```bash
NEWS_API_KEY="paste your api key in here"
```

Step 1: Navigate to the Project Folder
Open your terminal and change the directory to the project folder:
```bash
cd /path/to/your/project
```

Step 2: Create a Virtual Environment
Create a virtual environment named myenv. This isolates your project's dependencies from the system-wide Python installation:
```bash
python3 -m venv myenv
```

Step 3: Activate the Virtual Environment
Activate the virtual environment to start using it:
```bash
source myenv/bin/activate
```

Step 4: Install Requirements
Install the project dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```

Step 5: Run the Server
Finally, run the development server:
```bash
python3 manage.py runserver
```




import requests
import tkinter as tk

# ========================
# Fill in your credentials
# ========================
CLIENT_ID = "2tyvbkli6jiiurfi8qb991o39cprgp"
CLIENT_SECRET = "uaq0z2b2xn04347z6wfx0vp8j2d2kp"
USERNAME = "KittyKubTwitch"
REFRESH_INTERVAL = 5  # seconds

# ========================
# Functions
# ========================

def get_oauth_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params).json()
    return response.get('access_token')

def get_user_id(username, token, client_id):
    url = f"https://api.twitch.tv/helix/users?login={username}"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers).json()
    return response['data'][0]['id']

def get_viewer_count(user_id, token, client_id):
    url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers).json()
    if response['data']:
        return response['data'][0]['viewer_count']
    else:
        return 0

def update_viewers():
    viewers = get_viewer_count(USER_ID, TOKEN, CLIENT_ID)
    if viewers == 0:
        viewer_label.config(text="Offline", fg="red")
    else:
        viewer_label.config(text=f"Viewers: {viewers}", fg="white")
    root.after(REFRESH_INTERVAL * 1000, update_viewers)

# ========================
# Main
# ========================
TOKEN = get_oauth_token(CLIENT_ID, CLIENT_SECRET)
if not TOKEN:
    raise Exception("Failed to get OAuth token. Check your Client ID and Secret.")

USER_ID = get_user_id(USERNAME, TOKEN, CLIENT_ID)

# GUI Setup
root = tk.Tk()
root.title("Twitch Viewer Count Overlay")
root.geometry("200x50+50+50")  # Width x Height + X + Y
root.configure(bg='black')
root.attributes("-topmost", True)      # Always on top
root.attributes("-transparentcolor", "black")  # Make black transparent
root.overrideredirect(True)            # Remove window borders

# Viewer Label
viewer_label = tk.Label(root, text="Viewers: 0", font=("Arial", 20), bg="black", fg="white")
viewer_label.pack()

# Start updating viewers
update_viewers()
root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
import csv
import webbrowser


class LibraryItem:
    """Class to represent a track in the library."""
    def __init__(self, id, name, artist, rating, youtube_link):
        self.id = id
        self.name = name
        self.artist = artist
        self.rating = float(rating) if isinstance(rating, (int, float)) else 0.0
        self.youtube_link = youtube_link

    def info(self):
        return f"{self.id}: {self.name} by {self.artist}, rating: {self.rating}"


# Global dictionaries to hold library and playlists
library = {}
playlists = {}


# Load tracks from a CSV file
def load_library_from_csv(csv_file):
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                library[row["id"]] = LibraryItem(
                    id=row["id"],
                    name=row["name"],
                    artist=row["artist"],
                    rating=row["rating"],
                    youtube_link=row["youtube_link"]
                )
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found. Starting with an empty library.")
    except Exception as e:
        print(f"Error loading CSV: {e}")


# Save tracks to a CSV file
def save_library_to_csv(csv_file):
    try:
        with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["id", "name", "artist", "rating", "youtube_link"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for track in library.values():
                writer.writerow({
                    "id": track.id,
                    "name": track.name,
                    "artist": track.artist,
                    "rating": track.rating,
                    "youtube_link": track.youtube_link
                })
    except Exception as e:
        print(f"Error saving CSV: {e}")


# Save playlists to a CSV file
def save_playlists_to_csv():
    try:
        with open("playlists.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["playlist_name", "track_ids"])
            for playlist_name, track_ids in playlists.items():
                if isinstance(track_ids, list):
                    writer.writerow([playlist_name, ",".join(track_ids)])
    except Exception as e:
        print(f"Error saving playlists: {e}")


# Load playlists from CSV
def load_playlists_from_csv():
    try:
        with open("playlists.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                playlists[row["playlist_name"]] = row["track_ids"].split(",")
    except FileNotFoundError:
        print("Playlists file not found. Starting with an empty playlist.")
    except Exception as e:
        print(f"Error loading playlists: {e}")


# Play track function
def play_track(key):
    if key in library:
        youtube_link = library[key].youtube_link
        if youtube_link:
            webbrowser.open(youtube_link)
        else:
            messagebox.showerror("Error", "No YouTube link for this track.")
    else:
        messagebox.showerror("Error", "Track not found!")


class JukeBoxApp:
    """Main application class."""
    def __init__(self, window):
        window.geometry("900x600")
        window.title("JukeBox")
        window.configure(bg="lightblue")

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(expand=True, fill="both")

        # View Tracks Tab
        self.view_frame = tk.Frame(self.notebook, bg="lightblue")
        self.notebook.add(self.view_frame, text="View Tracks")

        self.view_track_listbox = tk.Listbox(self.view_frame, width=100, height=20)
        self.view_track_listbox.pack(pady=10)

        self.view_button = tk.Button(self.view_frame, text="Load Tracks", command=self.load_tracks)
        self.view_button.pack(pady=10)

        # Playlist Management Tab
        self.playlist_frame = tk.Frame(self.notebook, bg="lightblue")
        self.notebook.add(self.playlist_frame, text="Playlist Management")

        # Playlist Name Entry
        self.playlist_name_entry = tk.Entry(self.playlist_frame, width=30)
        self.playlist_name_entry.pack(pady=5)

        self.create_playlist_button = tk.Button(
            self.playlist_frame, text="Create Playlist", command=self.create_playlist
        )
        self.create_playlist_button.pack(pady=5)

        # Song Listbox for adding to playlist
        self.song_listbox = tk.Listbox(self.playlist_frame, width=100, height=10, selectmode=tk.MULTIPLE)
        self.song_listbox.pack(pady=5)

        # Add to Playlist Button
        self.add_to_playlist_button = tk.Button(
            self.playlist_frame, text="Add to Playlist", command=self.add_to_playlist
        )
        self.add_to_playlist_button.pack(pady=5)

        # Play Playlist Button
        self.play_playlist_button = tk.Button(
            self.playlist_frame, text="Play Playlist", command=self.play_playlist
        )
        self.play_playlist_button.pack(pady=5)

        # Delete Playlist Button
        self.delete_playlist_button = tk.Button(
            self.playlist_frame, text="Delete Playlist", command=self.delete_playlist
        )
        self.delete_playlist_button.pack(pady=5)

        # Playlist Names Listbox
        self.playlist_names_listbox = tk.Listbox(self.playlist_frame, width=50, height=10)
        self.playlist_names_listbox.pack(side=tk.LEFT, padx=5, pady=5)
        self.playlist_names_listbox.bind("<<ListboxSelect>>", self.show_playlist_songs)

        # Playlist Songs Listbox
        self.playlist_songs_listbox = tk.Listbox(self.playlist_frame, width=50, height=10)
        self.playlist_songs_listbox.pack(side=tk.RIGHT, padx=5, pady=5)

        # Update Tab
        self.update_frame = tk.Frame(self.notebook, bg="lightblue")
        self.notebook.add(self.update_frame, text="Update Tracks")

        # Input Fields for Update
        tk.Label(self.update_frame, text="Track ID:", bg="lightblue").pack(pady=5)
        self.track_id_entry = tk.Entry(self.update_frame, width=50)
        self.track_id_entry.pack(pady=5)

        tk.Label(self.update_frame, text="Track Name:", bg="lightblue").pack(pady=5)
        self.track_name_entry = tk.Entry(self.update_frame, width=50)
        self.track_name_entry.pack(pady=5)

        tk.Label(self.update_frame, text="YouTube Link:", bg="lightblue").pack(pady=5)
        self.track_link_entry = tk.Entry(self.update_frame, width=50)
        self.track_link_entry.pack(pady=5)

        self.update_track_button = tk.Button(
            self.update_frame, text="Add/Update Track", command=self.add_or_update_track
        )
        self.update_track_button.pack(pady=10)

        # Delete Tab
        self.delete_frame = tk.Frame(self.notebook, bg="lightblue")
        self.notebook.add(self.delete_frame, text="Delete Tracks")

        # Input Fields for Delete
        tk.Label(self.delete_frame, text="Track ID:", bg="lightblue").pack(pady=5)
        self.delete_track_id_entry = tk.Entry(self.delete_frame, width=50)
        self.delete_track_id_entry.pack(pady=5)

        tk.Label(self.delete_frame, text="Track Name:", bg="lightblue").pack(pady=5)
        self.delete_track_name_entry = tk.Entry(self.delete_frame, width=50)
        self.delete_track_name_entry.pack(pady=5)

        self.delete_track_button = tk.Button(
            self.delete_frame, text="Delete Track", command=self.delete_track
        )
        self.delete_track_button.pack(pady=10)

        # Load library and playlists
        load_library_from_csv("playlist.csv")
        load_playlists_from_csv()
        self.load_tracks()
        self.update_playlist_names_listbox()

    def load_tracks(self):
        """Load tracks from the library into the Listboxes."""
        self.view_track_listbox.delete(0, tk.END)
        self.song_listbox.delete(0, tk.END)
        for key, track in library.items():
            display_text = f"{track.id} - {track.name} by {track.artist}"
            self.view_track_listbox.insert(tk.END, display_text)
            self.song_listbox.insert(tk.END, display_text)

    def update_playlist_names_listbox(self):
        """Update the Playlist Names Listbox."""
        self.playlist_names_listbox.delete(0, tk.END)
        for playlist_name in playlists.keys():
            self.playlist_names_listbox.insert(tk.END, playlist_name)

    def show_playlist_songs(self, event):
        """Display songs in the selected playlist."""
        selected_index = self.playlist_names_listbox.curselection()
        if selected_index:
            playlist_name = self.playlist_names_listbox.get(selected_index)
            self.playlist_songs_listbox.delete(0, tk.END)
            if playlist_name in playlists:
                track_ids = playlists[playlist_name]
                for track_id in track_ids:
                    if track_id in library:
                        track = library[track_id]
                        self.playlist_songs_listbox.insert(tk.END, f"{track.id} - {track.name} by {track.artist}")

    def create_playlist(self):
        """Create a new playlist."""
        playlist_name = self.playlist_name_entry.get().strip()
        if not playlist_name:
            messagebox.showerror("Error", "Please enter a playlist name.")
            return

        if playlist_name in playlists:
            messagebox.showerror("Error", f"Playlist '{playlist_name}' already exists.")
        else:
            playlists[playlist_name] = []
            save_playlists_to_csv()
            self.update_playlist_names_listbox()
            messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully.")

    def add_to_playlist(self):
        """Add selected songs to the playlist."""
        selected_indices = self.song_listbox.curselection()
        playlist_name = self.playlist_name_entry.get().strip()

        if not playlist_name:
            messagebox.showerror("Error", "Please enter a playlist name.")
            return

        if playlist_name not in playlists:
            playlists[playlist_name] = []

        if selected_indices:
            for index in selected_indices:
                song_id = self.song_listbox.get(index).split(" - ")[0]  # Extract song ID
                if song_id not in playlists[playlist_name]:
                    playlists[playlist_name].append(song_id)

            save_playlists_to_csv()
            self.update_playlist_names_listbox()
            messagebox.showinfo("Success", f"Songs added to playlist '{playlist_name}'.")
        else:
            messagebox.showerror("Error", "No songs selected.")

    def delete_playlist(self):
        """Delete the selected playlist."""
        selected_index = self.playlist_names_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a playlist to delete.")
            return

        playlist_name = self.playlist_names_listbox.get(selected_index)
        if playlist_name in playlists:
            del playlists[playlist_name]
            save_playlists_to_csv()
            self.update_playlist_names_listbox()
            self.playlist_songs_listbox.delete(0, tk.END)  # Clear songs in the deleted playlist
            messagebox.showinfo("Success", f"Playlist '{playlist_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Playlist not found.")

    def add_or_update_track(self):
        """Add or update a track in the library."""
        track_id = self.track_id_entry.get().strip()
        track_name = self.track_name_entry.get().strip()
        track_link = self.track_link_entry.get().strip()

        if not track_id or not track_name or not track_link:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if track_id in library:
            library[track_id].name = track_name
            library[track_id].youtube_link = track_link
            messagebox.showinfo("Success", f"Track '{track_id}' updated successfully.")
        else:
            library[track_id] = LibraryItem(
                id=track_id, name=track_name, artist="Unknown", rating=0, youtube_link=track_link
            )
            messagebox.showinfo("Success", f"Track '{track_id}' added successfully.")

        save_library_to_csv("playlist.csv")
        self.load_tracks()

    def delete_track(self):
        """Delete a track from the library and playlists."""
        track_id = self.delete_track_id_entry.get().strip()
        track_name = self.delete_track_name_entry.get().strip()

        if not track_id or not track_name:
            messagebox.showerror("Error", "Please fill in both ID and Name.")
            return

        if track_id in library and library[track_id].name == track_name:
            del library[track_id]
            for playlist_name in playlists:
                playlists[playlist_name] = [id_ for id_ in playlists[playlist_name] if id_ != track_id]

            save_library_to_csv("playlist.csv")
            save_playlists_to_csv()
            self.load_tracks()
            self.update_playlist_names_listbox()
            messagebox.showinfo("Success", f"Track '{track_id}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Track ID and Name do not match any track.")

    def play_playlist(self):
        """Play all songs in the selected playlist."""
        selected_index = self.playlist_names_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a playlist to play.")
            return

        playlist_name = self.playlist_names_listbox.get(selected_index)
        if playlist_name in playlists:
            for track_id in playlists[playlist_name]:
                play_track(track_id)
        else:
            messagebox.showerror("Error", "Playlist not found.")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = JukeBoxApp(root)
    root.mainloop()

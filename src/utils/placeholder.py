import customtkinter as ctk


class PlaceholderText:
    def __init__(self, text_widget, placeholder_text):
        self.text_widget = text_widget
        self.placeholder_text = placeholder_text

        if isinstance(self.text_widget, ctk.CTkEntry):
            self.text_widget.insert(0, self.placeholder_text)
            self.clear_placeholder = self.clear_entry_placeholder
            self.restore_placeholder = self.restore_entry_placeholder
        elif isinstance(self.text_widget, ctk.CTkTextbox):
            self.text_widget.insert("1.0", self.placeholder_text)
            self.clear_placeholder = self.clear_text_placeholder
            self.restore_placeholder = self.restore_text_placeholder

        self.text_widget.bind("<FocusIn>", self.clear_placeholder)
        self.text_widget.bind("<FocusOut>", self.restore_placeholder)

    def clear_entry_placeholder(self, event):
        if self.text_widget.get() == self.placeholder_text:
            self.text_widget.delete(0, "end")

    def restore_entry_placeholder(self, event):
        if not self.text_widget.get().strip():
            self.text_widget.insert(0, self.placeholder_text)

    def clear_text_placeholder(self, event):
        if self.text_widget.get("1.0", "end-1c") == self.placeholder_text:
            self.text_widget.delete("1.0", "end")

    def restore_text_placeholder(self, event):
        if not self.text_widget.get("1.0", "end-1c").strip():
            self.text_widget.insert("1.0", self.placeholder_text)

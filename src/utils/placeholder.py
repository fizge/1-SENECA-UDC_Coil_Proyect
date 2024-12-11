import customtkinter as ctk


class PlaceholderText:
    """
    A class to manage placeholder text for `customtkinter` widgets (`CTkEntry` and `CTkTextbox`).

    This class adds placeholder functionality to text input widgets. The placeholder text
    appears when the widget is empty and is automatically removed when the widget gains focus.
    The placeholder reappears if the widget loses focus while empty.

    Attributes:
        text_widget: The `customtkinter` widget (`CTkEntry` or `CTkTextbox`) to which the 
                     placeholder functionality is added.
        placeholder_text: The placeholder text to display in the widget.
    """

    def __init__(self, text_widget, placeholder_text):
        """
        Initializes the `PlaceholderText` class.

        Depending on the type of `text_widget`, the placeholder text is inserted at the 
        appropriate position. Focus event bindings are added to manage the placeholder behavior.

        :param text_widget: The `customtkinter` widget (`CTkEntry` or `CTkTextbox`).
        :param placeholder_text: The placeholder text to display in the widget.
        """
        self.text_widget = text_widget
        self.placeholder_text = placeholder_text

        # Determine the widget type and configure placeholder handling
        if isinstance(self.text_widget, ctk.CTkEntry):
            self.text_widget.insert(0, self.placeholder_text)  # Insert placeholder in `CTkEntry`
            self.clear_placeholder = self.clear_entry_placeholder
            self.restore_placeholder = self.restore_entry_placeholder
        elif isinstance(self.text_widget, ctk.CTkTextbox):
            self.text_widget.insert("1.0", self.placeholder_text)  # Insert placeholder in `CTkTextbox`
            self.clear_placeholder = self.clear_text_placeholder
            self.restore_placeholder = self.restore_text_placeholder

        # Bind focus events to placeholder handling methods
        self.text_widget.bind("<FocusIn>", self.clear_placeholder)
        self.text_widget.bind("<FocusOut>", self.restore_placeholder)

    def clear_entry_placeholder(self, event):
        """
        Clears the placeholder text in a `CTkEntry` widget when it gains focus,
        if the current text matches the placeholder.

        :param event: The focus event triggering this method.
        """
        if self.text_widget.get() == self.placeholder_text:
            self.text_widget.delete(0, "end")

    def restore_entry_placeholder(self, event):
        """
        Restores the placeholder text in a `CTkEntry` widget when it loses focus,
        if the widget is empty.

        :param event: The focus event triggering this method.
        """
        if not self.text_widget.get().strip():  # Check if the entry is empty
            self.text_widget.insert(0, self.placeholder_text)

    def clear_text_placeholder(self, event):
        """
        Clears the placeholder text in a `CTkTextbox` widget when it gains focus,
        if the current text matches the placeholder.

        :param event: The focus event triggering this method.
        """
        if self.text_widget.get("1.0", "end-1c") == self.placeholder_text:
            self.text_widget.delete("1.0", "end")

    def restore_text_placeholder(self, event):
        """
        Restores the placeholder text in a `CTkTextbox` widget when it loses focus,
        if the widget is empty.

        :param event: The focus event triggering this method.
        """
        if not self.text_widget.get("1.0", "end-1c").strip():  # Check if the textbox is empty
            self.text_widget.insert("1.0", self.placeholder_text)

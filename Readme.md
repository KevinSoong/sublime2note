Save to Evernote
===
### Save your Evernotes from Sublime Text 2

#### Introduction

**Save to Evernote** is a Sublime Text 2 plugin that helps you saving files from Sublime Text 2 to your Evernote account.

By default, it adds a command under *File > Save to Evernote*, with a default shortcut: *cmd+alt+shift+e*. Each time you perform the command, it will create an note based on the editing file.

#### Authentication

The first time you use this plugin, it will prompt an webpage for authentication from the offical Evernote API. You can change the length of the authentication, from 1 day to 1 year. Once it's done, you can save the note without this step for as long as you liked.

##### Privacy
All the authentication information will be stored locally in you machine. This plugin does not send your Evernote access token over the cloud. However, if you finished working on an untrusted machine, please remember to perform the **Reset Evernote Authentication** command under *Preference > Package Settings > Save to Evernote* to protect your account.

#### Customization

You can customize **Save to Evernote** at *Preference > Package Settings > Save to Evernote* with customized key bindings or more advanced features.

#####Advanced Features:
* always_use_filename_as_title: Use filename as note title and save your note without any prompt interruption.
* always_prompt_for_tags: Ask for tags when saving the note.


If you have any question please contact me at: sublime2note(at)gmail.com


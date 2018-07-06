# PYPASSVAULT

A simple command line password vault written in python.

## Description

This tool was developed as a personal experiment to try out cryptography in python and also to develop a handy tool that can act as a secure command line password vault.

## Installation

```
pip install pypassvault
```

## Usage

Once you install the package, you will can use ```passvault``` utility from command line to use this tool.

- Help

```
> passvault -h
Usage: passvault [--core-opts] <subcommand> [--subcommand-opts] ...

Core options:

  --complete                     Print tab-completion candidates for given parse remainder.
  --hide=STRING                  Set default value of run()'s 'hide' kwarg.
  --write-pyc                    Enable creation of .pyc files.
  -d, --debug                    Enable debug output.
  -e, --echo                     Echo executed commands before running.
  -f STRING, --config=STRING     Runtime configuration file to use.
  -h [STRING], --help[=STRING]   Show core or per-task help and exit.
  -l, --list                     List available tasks.
  -p, --pty                      Use a pty when executing shell commands.
  -V, --version                  Show version and exit.
  -w, --warn-only                Warn, instead of failing, when shell commands fail.

Subcommands:

  configure   Set the configuration
  get         Get password for a username and application (optional)
  list        List all applications and users for which password is set
  setpasswd   Set password for a username and application (optional)
```

If you need help on any sub command you can type ```passvalut -h <subcommand>``` to see the specific help for it.

e.g.
```
> passvault -h configure
Usage: passvault [--core-opts] configure [--options] [other tasks here ...]

Docstring:
  Set the configuration

Options:
  -c STRING, --confdir=STRING
```

- Set a password
```
passvault setpasswd -a appname -u username
Enter vault password:
Set an app password for username:
```

When you run passvault for the first time you will be asked to set up a vault password. Please note that Vault password is the single password that you will need for all future operations. 

**Please do not forget your _vault password_ as if you forget it then the vault will not be recoverable.**

- Get the password details

```
> passvault get -a appname -u username
Enter vault password:
<Password>
```
- List Applications and Usernames present under passvault

```
> passvault list -a appname
Enter valult password:
Users for application appname are:
['username']
```
To list all applications & Usernames

```
> passvault list
```

- To check pypassvault version

```
passvault -V or passvault --version
```

## Todo

- Refactoring of existing APIs
- Functionality of deleting records by appname or user - Completed
- Generate password feature
- Import and Export of Data
- Better Documentation
- Providing an API interface for passvault
- Improvement in Encryption & Portability of Password Vault
- Support for Clipboard
- Testing

**Better to have features:**

- Password expiration notification/reminder
- UI for pypassvault
- Cloud Backup & Sync of Vault File

## LICENSE

MIT
from django import dispatch

user_activated = dispatch.Signal(providing_args=["user"])
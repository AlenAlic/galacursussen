from flask import render_template
from backend.email import send_email


def send_reminder_email(user):
    send_email('Available courses', recipients=[user.email],
               text_body=render_template('email/reminder.txt', user=user),
               html_body=render_template('email/reminder.html', user=user))


def send_assignments_email(user, incie_courses, salcie_courses, committee=""):
    send_email('Upcoming courses', recipients=[user.email],
               text_body=render_template('email/assignments.txt', user=user, incie_courses=incie_courses,
                                         salcie_courses=salcie_courses, committee=committee),
               html_body=render_template('email/assignments.html', user=user, incie_courses=incie_courses,
                                         salcie_courses=salcie_courses, committee=committee))

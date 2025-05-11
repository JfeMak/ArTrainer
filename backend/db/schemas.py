'''
Users Schema:
id: String, Required, Unique
email: String, Required, Unique
username: String, Required, Unique
password: String, Required
created_at: Date, Required

Plans Schema:
id: String, Required, Unique
user_id: String, Required
title: String, Required
days: Int, Required
created_at: Data, Required

Tasks Schema:
id: String, Required, Unique
plan_id: String, Required
day: Int, Required
description: String, Required
completed: Boolean, Required

'''
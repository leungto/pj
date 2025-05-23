# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class Bookings(models.Model):
#     user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
#     seat = models.ForeignKey('Seats', models.DO_NOTHING, blank=True, null=True)
#     start_time = models.DateTimeField(blank=True, null=True)
#     end_time = models.DateTimeField(blank=True, null=True)
#     status = models.CharField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'bookings'


# class Reservations(models.Model):
#     id = models.CharField(primary_key=True)
#     user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
#     seat = models.ForeignKey('Seats', models.DO_NOTHING, blank=True, null=True)
#     date = models.DateField()
#     time_slot = models.ForeignKey('TimeSlots', models.DO_NOTHING, blank=True, null=True)
#     status = models.CharField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'reservations'


# class Rooms(models.Model):
#     name = models.CharField(blank=True, null=True)
#     location = models.CharField(blank=True, null=True)
#     capacity = models.IntegerField(blank=True, null=True)
#     is_active = models.BooleanField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'rooms'


# class Seats(models.Model):
#     room = models.ForeignKey(Rooms, models.DO_NOTHING, blank=True, null=True)
#     seat_number = models.CharField(blank=True, null=True)
#     is_available = models.BooleanField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'seats'


# class TimeSlots(models.Model):
#     id = models.CharField(primary_key=True)
#     start_time = models.CharField()
#     end_time = models.CharField()
#     name = models.CharField()
#     description = models.CharField(blank=True, null=True)
#     is_active = models.BooleanField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'time_slots'


# class Users(models.Model):
#     username = models.CharField(unique=True, blank=True, null=True)
#     email = models.CharField(unique=True, blank=True, null=True)
#     hashed_password = models.CharField(blank=True, null=True)
#     is_active = models.BooleanField(blank=True, null=True)
#     is_admin = models.BooleanField(blank=True, null=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'users'

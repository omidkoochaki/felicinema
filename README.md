
# FeliCinema

FeliCinema is a platform for those who love watching movies with other people and making new friendships based on this common interest.

People who have a house and a machine to show movies with it, can add Cinema to the platform. Define Cinema Sessions and how many people they can host in their private cinema. Also they can specify the settings of seats in their cinema and there is an option to check if the seat is wheelchair-friendly or not for every single seat.

Other people can search for cinemas, movies or cinema sessions and choose to make a reservation, the cinema owner will received an email and a accept-reservation link with security code to accept/reject reservants. Once the reservation request accepted by the Cinema Owner, reservant will be informed through the email.

Also, the Cinema Owner has a dashboard to see all reservations and accept/reject them without the need for a security code. Once the Cinema Owner accepts a reservation can add the reservant to his/her auto-accept reservation list.

When a reservant is in auto accept reservation list of one cinema owner, system accepts his/her reservation requests automatically.
## API Reference

### Cinema
#### Add Cinema
```http
  POST /cinema/add
```
- User must be Authenticated

| Parameter | Type     | Description   |
|:----------|:---------|:--------------|
| `title`   | `string` | **Required**. |
| `address` | `string` | **Required**. |


#### Add Cinema Seats
```http
  POST /cinema/add/<int:cinema_id>/seats/
```
- User must be cinema owner
- each list in main list stands for a seat row
- each number stands for a seat
- 1 stands fot whellchair-friendly and 0 for not.

| Parameter | Type   | Description                                             |
|:----------|:-------|:--------------------------------------------------------|
| `style`   | `JSON` | **Required**. a list of lists containing numbers 0 or 1 |

#### See Cinema List and Search
```http
  GET /cinema/all/?tile='',address=''
```
- User must be Authenticated
- query params are optional

#### See One Cinema
```http
  GET /cinema/cinema_id/
```
- User must be Authenticated


### Movie
#### Add New Movie
```http
  POST /cinema/movie/add/
```
- User must have a Cinema

| Parameter  | Type     | Description                       |
|:-----------|:---------|:----------------------------------|
| `title`    | `string` | **Required**.                     |
| `genre`    | `string` | **Required**.                     |
| `duration` | `string` | **Required**. Example: "02:30:00" |
| `summary`  | `string` | **Required**.                     |
| `language` | `string` | **Required**. Accepts E, P or O   |

#### See Movie List and Details
```http
  details: GET /cinema/movie/movie_id/
```
```http
  list: GET /cinema/movie/all/
```
- User must be authenticated

### Sessions
#### Add Cinema Session
```http
  POST /cinema/cinema_id/sessions/add/
```
- User must be cinema owner

| Parameter     | Type     | Description                                   |
|:--------------|:---------|:----------------------------------------------|
| `movie`       | `int`    | **Required**. Example: 2                      |
| `date`        | `string` | **Required**. Example: "1400-02-23"           |
| `time`        | `string` | **Required**. Example: "16:30:00"             |
| `translation` | `string` | **Required**. Accepts: PS, ES, OS, PV, EV, OV |
| `description` | `string` |                                               |
- 'PS', 'Persian Subtitle'
- 'ES', 'English Subtitle'
- 'OS', 'Other Subtitle'
- 'PV', 'Persian Voice'
- 'EV', 'English Voice'
- 'OV', 'Other Voice'

#### See Sessions List
```http
  GET /cinema/cinema_id/sessions/
```
- User must be Authenticated
- just shows sessions for future from right now

#### Reserve a session
```http
  POST /cinema/cinema_id/sessions/session_id/reserve
```
- User must be Authenticated

| Parameter | Type  | Description              |
|:----------|:------|:-------------------------|
| `seat_id` | `int` | **Required**. Example: 2 |


### Reservation
#### Get Reservation Info to Accept or Reject with Security Key
```http
  GET /cinema/reservation/uuid/
```
- User must has a cinema
- returns {'payment': payment_data}

#### Accept or Reject with Security Key
```http
  POST /cinema/reservation/uuid/
```
- User must have a cinema

| Parameter | Type   | Description                                |
|:----------|:-------|:-------------------------------------------|
| `is_paid` | `book` | **Required**. True/false for accept/reject |


## Running Tests

To run tests, run the following command

```bash
  django
```


## Deployment

To deploy this project run

```bash
  docker
```


## Feedback

If you have any feedback, please reach out to me at omid.koochaki@gmail.com


## 🚀 About Me
I'm a full stack developer with experience in Django, Fast API and Angular


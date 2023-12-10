# interview-test-ms

## Assignment description
The European Central Bank (ECB) puts out a file with FX rates in a date vs currency CSV file under https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip
- Create a simple REST API with a single endpoint that returns data to a user based on currency and date requests
- Please make currency mandatory and date optional. If both are provided then please return one single value, if date is not provided then please return all data for the given currency.
- Data to be fetched once at the start of the process and should be kept in the memory
 
Please write a simple solution using Python 3 paying attention to the following points:
- Code is maintainable and easy to read
- Simple documentation is available in your code base
- Appropriate tests are included in your code base covering the main features of your solution

## How to run
- Install requirements using `pip install -r requirements.txt`
- run `app.py`

(tested on Python 3.10)

## Usage
You can access the FX rates for a specific currency by going to http://localhost:5000/fxrates/<CURR>.

Example:

http://localhost:5000/fxrates/HUF

```json
{
  "1999-01-04": 251.48,
  "1999-01-05": 250.8,
  "1999-01-06": 250.67,
  "1999-01-07": 250.09,
  "1999-01-08": 250.15,
  "1999-01-11": 249.7,
  "1999-01-12": 249.2,
  ...
}
```

You can also query a single date by using the `date` url parameter

Example:

http://localhost:5000/fxrates/HUF?date=2023-12-08

```
381.9
```

If the specified currency or date is not found, the server will respond with 404 status code.
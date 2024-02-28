# RLT

## Project Overview

RLT is Python project to aggregate employee salary data into MangoDB.

## Main Features

- **Telegram Bot**: The bot is designed to interact with users on Telegram. It can receive JSON messages with specific fields and perform actions based on the received data.
- **Data Aggregation**: The project includes functionality for aggregating salary data from a MongoDB database. It supports different aggregation types such as hourly, daily, monthly, and weekly.
- **Asynchronous Operations**: The bot and data processing are implemented using Python's asyncio library, allowing for efficient handling of I/O-bound tasks.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Set up the MongoDB database and ensure that the connection string in `master.py` is correct.
4. Run the bot by executing `python bot.py`.

## Usage

To use the bot, send a JSON message to the bot with the following fields:

- `dt_from`: The start date for the data aggregation in ISO format.
- `dt_upto`: The end date for the data aggregation in ISO format.
- `group_type`: The type of aggregation to perform (e.g., "hour", "day", "month", "week").

The bot will respond with the aggregated data or an error message if the request is not valid.

## Example

Here's an example of how to use the bot:

1. Start the bot by running `python bot.py`.
2. Send a JSON message to the bot with the required fields. For example:

```json
{
 "dt_from": "2022-09-01T00:00:00",
 "dt_upto": "2022-12-31T23:59:00",
 "group_type": "month"
}
```

3. The bot will respond with the aggregated salary data for the specified date range and group type.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the terms of the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or concerns, please open an issue on GitHub.

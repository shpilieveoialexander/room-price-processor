import json
import logging

# Set up the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)


class DataLoader:
    """
    A class responsible for loading and validating JSON data from a file.

    Attributes:
    ----------
    file_path : str
        The path to the JSON file to be loaded.
    data : dict or None
        The loaded JSON data, initially set to None.
    """

    def __init__(self, file_path):
        """
        Initializes the DataLoader with a file path.

        Parameters:
        ----------
        file_path : str
            The path to the JSON file containing data.
        """
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """
        Loads data from the specified JSON file and validates it.

        Returns:
        -------
        dict
            The validated JSON data.

        Raises:
        ------
        ValueError
            If the data does not meet validation requirements.
        """
        logger.info("Loading data from file: %s", self.file_path)
        with open(self.file_path, "r") as file:
            self.data = json.load(file)

        self.validate_data()
        logger.info("Data loaded and validated successfully.")
        return self.data

    def validate_data(self):
        """
        Validates the loaded JSON data to ensure it has the required structure.

        Raises:
        ------
        ValueError
            If the data is missing required fields or has an incorrect structure.
        """
        logger.info("Validating data structure.")
        if "assignment_results" not in self.data or not isinstance(
                self.data["assignment_results"], list):
            logger.error("Invalid data: 'assignment_results' must be a list.")
            raise ValueError(
                "Invalid data: 'assignment_results' must be a list.")

        if not self.data["assignment_results"]:
            logger.error("Invalid data: 'assignment_results' is empty.")
            raise ValueError("Invalid data: 'assignment_results' is empty.")

        required_keys = [
            "shown_price", "net_price", "number_of_guests", "ext_data"
        ]
        for item in self.data["assignment_results"]:
            for key in required_keys:
                if key not in item:
                    logger.error(
                        "Invalid data: Missing key '%s' in assignment results.",
                        key)
                    raise ValueError(
                        f"Invalid data: Missing key '{key}' in assignment results.")
            if not isinstance(item["shown_price"], dict) or not item[
                "shown_price"]:
                logger.error(
                    "Invalid data: 'shown_price' must be a non-empty dictionary.")
                raise ValueError(
                    "Invalid data: 'shown_price' must be a non-empty dictionary.")
            if not isinstance(item["net_price"], dict) or not item[
                "net_price"]:
                logger.error(
                    "Invalid data: 'net_price' must be a non-empty dictionary.")
                raise ValueError(
                    "Invalid data: 'net_price' must be a non-empty dictionary.")
            if not isinstance(item["number_of_guests"], int):
                logger.error(
                    "Invalid data: 'number_of_guests' must be an integer.")
                raise ValueError(
                    "Invalid data: 'number_of_guests' must be an integer.")
            if not isinstance(item["ext_data"], dict) or "taxes" not in item[
                "ext_data"]:
                logger.error(
                    "Invalid data: 'ext_data' must contain a 'taxes' dictionary.")
                raise ValueError(
                    "Invalid data: 'ext_data' must contain a 'taxes' dictionary.")
        logger.info("Data validation completed successfully.")


class RoomProcessor:
    """
    A class responsible for processing room data from assignment results.

    Attributes:
    ----------
    assignment_results : dict
        The JSON object containing assignment results.
    shown_prices : dict
        Dictionary of room types and their shown prices.
    net_prices : dict
        Dictionary of room types and their net prices.
    taxes : dict
        Dictionary of applicable taxes parsed from JSON.
    number_of_guests : int
        The number of guests for the hotel stay.
    """

    def __init__(self, assignment_results):
        """
        Initializes the RoomProcessor with assignment result data.

        Parameters:
        ----------
        assignment_results : dict
            The JSON object containing the assignment result data.
        """
        self.assignment_results = assignment_results
        self.shown_prices = assignment_results["shown_price"]
        self.net_prices = assignment_results["net_price"]
        self.taxes = json.loads(assignment_results["ext_data"]["taxes"])
        self.number_of_guests = assignment_results["number_of_guests"]

    def find_cheapest_room(self):
        """
        Finds the room with the lowest shown price.

        Returns:
        -------
        dict
            A dictionary with the room type, price, and number of guests.
        """
        logger.info("Finding the cheapest room.")
        cheapest_price = float("inf")
        cheapest_room_type = ""

        for room, price in self.shown_prices.items():
            price = float(price)
            if price < cheapest_price:
                cheapest_price = price
                cheapest_room_type = room

        logger.info("Cheapest room found: %s with price %f",
                    cheapest_room_type, cheapest_price)
        return {
            "room_type": cheapest_room_type,
            "price": round(cheapest_price, 2),
            "number_of_guests": self.number_of_guests
        }

    def calculate_total_prices(self):
        """
        Calculates the total price for each room, including taxes.

        Returns:
        -------
        dict
            A dictionary where each key is a room type and each value is another
            dictionary containing the net price and total price (net price + taxes).
        """
        logger.info("Calculating total prices for each room.")
        total_prices = {}
        total_taxes = sum(float(value) for value in self.taxes.values())

        for room, net_price in self.net_prices.items():
            total_price = float(net_price) + total_taxes
            total_prices[room] = {
                "net_price": net_price,
                "total_price_with_taxes": round(total_price, 2)
            }

        logger.info("Total prices calculated successfully.")
        return total_prices


class OutputHandler:
    """
    A class responsible for handling the output of data to a file.

    Attributes:
    ----------
    output_path : str
        The path to the file where output data will be saved.
    """

    def __init__(self, output_path):
        """
        Initializes the OutputHandler with an output file path.

        Parameters:
        ----------
        output_path : str
            The path to the file where output will be saved.
        """
        self.output_path = output_path

    def save_output(self, cheapest_room, total_prices):
        """
        Saves the processed room data and prices to a JSON file.

        Parameters:
        ----------
        cheapest_room : dict
            Information about the room with the lowest price.
        total_prices : dict
            Information on the total prices for all rooms.
        """
        output_data = {
            "cheapest_room": cheapest_room,
            "total_prices": total_prices
        }

        with open(self.output_path, "w") as outfile:
            json.dump(output_data, outfile, indent=4)
        logger.info("Output has been saved to %s", self.output_path)


if __name__ == '__main__':
    try:
        data_loader = DataLoader("data.json")
        data = data_loader.load_data()

        assignment_results = data["assignment_results"][0]
        room_processor = RoomProcessor(assignment_results)

        cheapest_room = room_processor.find_cheapest_room()
        total_prices = room_processor.calculate_total_prices()

        output_handler = OutputHandler("output.json")
        output_handler.save_output(cheapest_room, total_prices)

    except Exception as e:
        logger.error("An error occurred: %s", e)

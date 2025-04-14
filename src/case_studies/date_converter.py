from datetime import datetime

class DateConverter:
    """
    A class to convert dates between different formats
    """
    
    @staticmethod
    def convert(date_str, from_format, to_format):
        """
        Convert a date string from one format to another.
        
        Args:
            date_str (str): The date string to convert
            from_format (str): The format of the input date string
            to_format (str): The desired output format
            
        Returns:
            str: The converted date string
            
        Raises:
            ValueError: If the date string doesn't match the input format
                        or represents an invalid date
        """
        try:
            # Parse the date string using the input format
            date_obj = datetime.strptime(date_str, from_format)
            
            # Format the date object using the output format
            return date_obj.strftime(to_format)
        except ValueError as e:
            # Re-raise with a more descriptive message
            raise ValueError(f"Invalid date format or date: {date_str} does not match format {from_format}") from e

    @staticmethod
    def iso_to_dmy(date_str):
        """
        Convert a date from ISO format (YYYY-MM-DD) to DMY format (DD/MM/YYYY).
        
        Args:
            date_str (str): Date in ISO format (YYYY-MM-DD)
            
        Returns:
            str: Date in DMY format (DD/MM/YYYY)
        """
        return DateConverter.convert(date_str, "%Y-%m-%d", "%d/%m/%Y")

    @staticmethod
    def dmy_to_iso(date_str):
        """
        Convert a date from DMY format (DD/MM/YYYY) to ISO format (YYYY-MM-DD).
        
        Args:
            date_str (str): Date in DMY format (DD/MM/YYYY)
            
        Returns:
            str: Date in ISO format (YYYY-MM-DD)
        """
        return DateConverter.convert(date_str, "%d/%m/%Y", "%Y-%m-%d")
        
    @staticmethod
    def format_date(date_str, output_format):
        """
        Format a date string to the specified output format, with automatic input format detection.
        
        Args:
            date_str (str): The date string to format
            output_format (str): The desired output format
            
        Returns:
            str: The formatted date string
            
        Raises:
            ValueError: If the date string is empty or None, or if the format cannot be detected
        """
        if date_str is None or (isinstance(date_str, str) and date_str.strip() == ""):
            raise ValueError("Date string cannot be empty")
        
        # Try different common formats
        formats_to_try = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%m-%d-%Y"]
        
        for fmt in formats_to_try:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime(output_format)
            except ValueError:
                continue
        
        # If we get here, no format matched
        raise ValueError(f"Could not detect format of date string: {date_str}")
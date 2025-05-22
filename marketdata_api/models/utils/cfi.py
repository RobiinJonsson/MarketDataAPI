from enum import Enum
from dataclasses import dataclass
from typing import Optional

class Category(Enum):
    EQUITIES = 'E'
    DEBT = 'D'
    ENTITLEMENTS = 'R'
    OPTIONS = 'O'
    FUTURES = 'F'
    SWAPS = 'S'
    OTHERS = 'M'
    LOANS = 'L'

class Group(Enum):
    # Equities (E)
    SHARES = 'S'        # Shares
    PREFERRED = 'P'     # Preferred/Preference shares
    DEPOSITORY = 'D'    # Depositary receipts
    UNITS = 'U'         # Units
    ETF = 'F'           # Exchange traded funds
    OTHER_EQUITY = 'M'  # Others/Miscellaneous

    # Debt Instruments (D)
    BONDS = 'B'              # Basic bonds/debentures
    CONVERTIBLE_BONDS = 'C'  # Convertible bonds
    STRUCTURED = 'D'         # Deposit based bonds
    MEDIUM_TERM = 'G'        # Medium Term Notes
    MONEY_MARKET = 'Y'       # Money market instruments
    MUNICIPAL_BONDS = 'N'    # Municipal bonds
    OPTIONS = 'A'            # Asset backed securities
    MORTGAGE = 'T'           # Mortgage backed securities
    OTHER_DEBT = 'M'         # Others/Miscellaneous

    # Rights (R)
    RIGHT_SUBSCRIPTION = 'S'  # Subscription/Purchase
    RIGHT_ALLOTMENT = 'A'    # Allotment
    RIGHT_PURCHASE = 'B'     # Buy back
    RIGHT_PUT = 'P'          # Put option
    RIGHT_CALL = 'C'         # Call option
    RIGHT_WARRANT = 'W'      # Warrant
    RIGHT_OTHER = 'M'        # Others/Miscellaneous

    # Options (O)
    CALL_OPTIONS = 'C'       # Call options
    PUT_OPTIONS = 'P'        # Put options
    MULTI_LEG = 'M'          # Multi-leg options
    OTHER_OPTIONS = 'O'      # Others/Miscellaneous

    # Futures (F)
    FINANCIAL = 'F'          # Financial futures
    COMMODITIES = 'C'        # Commodity futures
    MULTI_LEG_FUTURES = 'M'  # Multi-leg futures
    OTHER_FUTURES = 'O'      # Others/Miscellaneous

    # Swaps (S)
    RATE_SWAPS = 'R'         # Interest rate swaps
    CREDIT_SWAPS = 'C'       # Credit default swaps
    CURRENCY_SWAPS = 'F'     # Foreign exchange swaps
    OTHER_SWAPS = 'O'        # Others/Miscellaneous

    # Non-standard (M)
    SPOT = 'S'               # Spot
    LOANS = 'L'              # Loans
    REFERENTIAL = 'R'        # Reference instruments
    OTHER_NON_STANDARD = 'O' # Others/Miscellaneous

class CategoryDescription(Enum):
    EQUITIES = "Equity"
    DEBT = "Debt"
    ENTITLEMENTS = "Entitlement (Right)"
    OPTIONS = "Option"
    FUTURES = "Future"
    SWAPS = "Swap"
    OTHERS = "Other"
    LOANS = "Loan"

class GroupDescription:
    DESCRIPTIONS = {
        # Equities (E)
        'ES': "Common/Ordinary Shares",
        'EP': "Preferred/Preference Shares",
        'ED': "Depositary Receipts",
        'EU': "Investment Fund Units",
        'EF': "Exchange Traded Fund Units",
        'EM': "Other Equity Instruments",
        
        # Debt (D)
        'DB': "Basic Bonds/Debentures",
        'DC': "Convertible Bonds",
        'DD': "Deposit Based Bonds",
        'DG': "Medium Term Notes",
        'DY': "Money Market Instruments",
        'DN': "Municipal Bonds",
        'DA': "Asset Backed Securities",
        'DT': "Mortgage Backed Securities",
        'DM': "Other Debt Instruments",
        
        # Rights (R)
        'RS': "Subscription/Purchase Rights",
        'RA': "Allotment Rights",
        'RB': "Buy Back Rights",
        'RP': "Put Option Rights",
        'RC': "Call Option Rights",
        'RW': "Warrant Rights",
        'RM': "Other Rights",
        
        # Options (O)
        'OC': "Call Options",
        'OP': "Put Options",
        'OM': "Multi-leg Options",
        'OO': "Other Options",
        
        # Futures (F)
        'FF': "Financial Futures",
        'FC': "Commodity Futures",
        'FM': "Multi-leg Futures",
        'FO': "Other Futures",
        
        # Swaps (S)
        'SR': "Interest Rate Swaps",
        'SC': "Credit Default Swaps",
        'SF': "Foreign Exchange Swaps",
        'SO': "Other Swaps",
        
        # Non-standard (M)
        'MS': "Spot Instruments",
        'ML': "Loan Instruments",
        'MR': "Reference Instruments",
        'MO': "Other Non-standard Instruments"
    }

class AttributeDescription:
    # Equity Attribute Positions
    VOTING_RIGHTS = {  # Position 3 for Equities
        'V': "Voting",
        'N': "Non-voting",
        'R': "Restricted voting",
        'E': "Enhanced voting",
        'X': "Not applicable",
    }
    
    OWNERSHIP_TRANSFER = {  # Position 4 for Equities
        'R': "Registered",
        'B': "Bearer",
        'X': "Not applicable",
    }
    
    DIVIDEND_STATUS = {  # Position 5 for Equities
        'F': "Full dividend",
        'P': "Partial dividend",
        'N': "No dividend",
        'X': "Not applicable",
    }
    
    PAYMENT_STATUS = {  # Position 6 for Equities
        'P': "Paid",
        'N': "Partly paid",
        'O': "Nil paid",
        'X': "Not applicable",
    }

    # Debt Attribute Positions
    DEBT_GUARANTEE = {  # Position 3 for Debt
        'T': "Guaranteed",
        'S': "Secured",
        'U': "Unsecured",
        'X': "Not applicable",
    }
    
    DEBT_INTEREST = {  # Position 4 for Debt
        'F': "Fixed rate",
        'Z': "Zero coupon",
        'V': "Variable rate",
        'I': "Inflation-linked",
        'X': "Not applicable",
    }
    
    DEBT_MATURITY = {  # Position 5 for Debt
        'D': "Less than 1 year",
        'Y': "1-5 years",
        'G': "Greater than 5 years",
        'P': "Perpetual",
        'X': "Not applicable",
    }
    
    DEBT_FORM = {  # Position 6 for Debt
        'B': "Bearer",
        'R': "Registered",
        'N': "Bearer/Registered",
        'X': "Not applicable",
    }

    # Options Attribute Positions
    OPTION_STYLE = {  # Position 3 for Options
        'A': "American",
        'B': "Bermuda",
        'E': "European",
        'X': "Not applicable",
    }
    
    OPTION_DELIVERY = {  # Position 4 for Options
        'P': "Physical",
        'C': "Cash",
        'X': "Not applicable",
    }
    
    OPTION_UNDERLYING = {  # Position 5 for Options
        'E': "Equities",
        'D': "Debt",
        'C': "Currency",
        'I': "Index",
        'R': "Interest rate",
        'M': "Commodities",
        'X': "Not applicable",
    }
    
    OPTION_SCHEME = {  # Position 6 for Options
        'S': "Standard",
        'E': "Exotic",
        'X': "Not applicable",
    }

    # Futures Attribute Positions - Updated with more detailed classifications
    FUTURES_SETTLEMENT = {  # Position 3 for Futures
        'P': "Physical",
        'C': "Cash",
        'N': "Non-Deliverable",
        'X': "Not applicable",
    }
    
    FUTURES_UNDERLYING_FINANCIAL = {  # Position 4 for Financial Futures (FF)
        'B': "Baskets",
        'S': "Stock-Equities",
        'D': "Debt Instruments",
        'C': "Currencies",
        'I': "Indices",
        'O': "Options",
        'F': "Futures",
        'W': "Swaps",
        'N': "Interest Rates",
        'V': "Stock Dividend",
        'M': "Others (Misc.)",
        'X': "Not applicable",
    }
    
    FUTURES_UNDERLYING_COMMODITIES = {  # Position 4 for Commodity Futures (FC)
        'E': "Extraction Resources",
        'A': "Agriculture",
        'I': "Industrial Products",
        'S': "Services",
        'N': "Environmental",
        'P': "Polypropylene Products",
        'H': "Generated Resources",
        'M': "Others (Misc.)",
        'X': "Not applicable",
    }
    
    FUTURES_DELIVERY = {  # Position 5 for Futures (fixed from position mapping error)
        'F': "Fixed date",
        'V': "Variable date",
        'P': "Physical delivery",  # Added to match your FFSP code
        'C': "Cash settlement",    # Added to be consistent
        'X': "Not applicable",
    }
    
    FUTURES_SCHEME = {  # Position 6 for Futures
        'S': "Standardized",
        'N': "Non-Standardized",
        'X': "Not applicable",
    }

    # Swaps Attribute Positions
    SWAP_SINGLE_SWING = {  # Position 3 for Swaps
        'S': "Single",
        'W': "Swing",
        'X': "Not applicable",
    }
    
    SWAP_RATE_TYPE = {  # Position 4 for Swaps
        'F': "Fixed/Fixed",
        'V': "Fixed/Variable",
        'L': "Variable/Variable",
        'X': "Not applicable",
    }
    
    SWAP_TERMS = {  # Position 5 for Swaps
        'C': "Constant notional",
        'V': "Variable notional",
        'X': "Not applicable",
    }
    
    SWAP_SCHEME = {  # Position 6 for Swaps
        'S': "Standard",
        'N': "Non-standard",
        'X': "Not applicable",
    }

    @classmethod
    def decode_equity_attributes(cls, attrs: tuple[str, str, str, str]) -> dict[str, str]:
        """Decode equity instrument attributes"""
        return {
            "voting_rights": cls.VOTING_RIGHTS.get(attrs[0], "Unknown"),
            "ownership": cls.OWNERSHIP_TRANSFER.get(attrs[1], "Unknown"),
            "dividend": cls.DIVIDEND_STATUS.get(attrs[2], "Unknown"),
            "payment": cls.PAYMENT_STATUS.get(attrs[3], "Unknown")
        }

    @classmethod
    def decode_debt_attributes(cls, attrs: tuple[str, str, str, str]) -> dict[str, str]:
        """Decode debt instrument attributes"""
        return {
            "guarantee": cls.DEBT_GUARANTEE.get(attrs[0], "Unknown"),
            "interest": cls.DEBT_INTEREST.get(attrs[1], "Unknown"),
            "maturity": cls.DEBT_MATURITY.get(attrs[2], "Unknown"),
            "form": cls.DEBT_FORM.get(attrs[3], "Unknown")
        }

    @classmethod
    def decode_option_attributes(cls, attrs: tuple[str, str, str, str]) -> dict[str, str]:
        """Decode option instrument attributes"""
        return {
            "style": cls.OPTION_STYLE.get(attrs[0], "Unknown"),
            "delivery": cls.OPTION_DELIVERY.get(attrs[1], "Unknown"),
            "underlying": cls.OPTION_UNDERLYING.get(attrs[2], "Unknown"),
            "scheme": cls.OPTION_SCHEME.get(attrs[3], "Unknown")
        }

    @classmethod
    def decode_futures_attributes(cls, attrs: tuple[str, str, str, str], cfi_code: str) -> dict[str, str]:
        """Decode futures instrument attributes with more detailed classifications"""
        
        # Get the underlying based on financial vs commodity future
        if cfi_code[:2] == "FF":
            underlying = f"Financial: {cls.FUTURES_UNDERLYING_FINANCIAL.get(attrs[0], 'Unknown')}"
        elif cfi_code[:2] == "FC":
            underlying = f"Commodity: {cls.FUTURES_UNDERLYING_COMMODITIES.get(attrs[0], 'Unknown')}"
        else:
            underlying = "Unknown"
        
        # Map positions correctly: pos3=underlying(already handled), pos4=delivery, pos5=standardization
        result = {
            "underlying": underlying,
            "delivery": cls.FUTURES_SETTLEMENT.get(attrs[1], "Unknown"),
            "scheme": cls.FUTURES_SCHEME.get(attrs[3], "Unknown")
        }
        
        return result

    @classmethod
    def decode_swap_attributes(cls, attrs: tuple[str, str, str, str]) -> dict[str, str]:
        """Decode swap instrument attributes"""
        return {
            "single_swing": cls.SWAP_SINGLE_SWING.get(attrs[0], "Unknown"),
            "rate_type": cls.SWAP_RATE_TYPE.get(attrs[1], "Unknown"),
            "terms": cls.SWAP_TERMS.get(attrs[2], "Unknown"),
            "scheme": cls.SWAP_SCHEME.get(attrs[3], "Unknown")
        }

@dataclass
class CFI:
    code: str
    category: Optional[Category] = None
    group: Optional[Group] = None

    def __post_init__(self):
        if len(self.code) != 6:
            raise ValueError("CFI code must be 6 characters")
        self.category = Category(self.code[0])
        self.group = Group(self.code[1])

    @property
    def attributes(self) -> tuple[str, str, str, str]:
        """Returns tuple of attribute characters (3rd to 6th position)"""
        return tuple(self.code[2:])

    def is_equity(self) -> bool:
        return self.category == Category.EQUITIES

    def is_debt(self) -> bool:
        return self.category == Category.DEBT

    def is_derivative(self) -> bool:
        return self.category in (Category.OPTIONS, Category.FUTURES)

    @property
    def category_description(self) -> str:
        """Returns human readable category description"""
        return CategoryDescription[self.category.name].value

    @property
    def group_description(self) -> str:
        """Returns human readable group description"""
        key = f"{self.category.value}{self.group.value}"
        return GroupDescription.DESCRIPTIONS.get(key, "Unknown Instrument Type")

    def describe(self) -> dict[str, str]:
        """Returns complete description of the instrument classification"""
        result = {
            "cfi_code": self.code,
            "category": self.category.value,
            "category_description": self.category_description,
            "group": self.group.value,
            "group_description": self.group_description,
        }
        
        # Add attribute descriptions based on category
        if self.is_equity():
            result["attributes"] = AttributeDescription.decode_equity_attributes(self.attributes)
        elif self.is_debt():
            result["attributes"] = AttributeDescription.decode_debt_attributes(self.attributes)
        elif self.category == Category.OPTIONS:
            result["attributes"] = AttributeDescription.decode_option_attributes(self.attributes)
        elif self.category == Category.FUTURES:
            result["attributes"] = AttributeDescription.decode_futures_attributes(self.attributes, self.code)
        elif self.category == Category.SWAPS:
            result["attributes"] = AttributeDescription.decode_swap_attributes(self.attributes)
        else:
            result["attributes"] = "".join(self.attributes)
            
        return result

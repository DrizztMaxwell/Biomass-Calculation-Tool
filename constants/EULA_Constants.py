import flet as ft

class EULA_Constants:
    """Constants for EULA styling and content."""
    # Colors
    PRIMARY_COLOR = ft.Colors.SECONDARY_CONTAINER
    HEADER_COLOR = ft.Colors.GREEN_700
    ERROR_COLOR = ft.Colors.RED_600
    BORDER_COLOR = ft.Colors.GREY_300
    TEXT_COLOR = ft.Colors.PRIMARY
    
    # Icons
    HEADER_ICON = ft.Icons.SECURITY
    TERMS_ICON = ft.Icons.DESCRIPTION
    DISCLAIMER_ICON = ft.Icons.WARNING_AMBER
    ACCEPTANCE_ICON = ft.Icons.CHECK_CIRCLE_OUTLINE
    EXIT_ICON = ft.Icons.EXIT_TO_APP
    
    # Sizes
    HEADER_SIZE = 32
    TITLE_SIZE = 24
    SUBTITLE_SIZE = 14
    SECTION_HEADING_SIZE = 16
    SECTION_TEXT_SIZE = 14
    EXIT_MESSAGE_SIZE = 16
    
    # Spacing
    SECTION_SPACING = 5
    BUTTON_SPACING = 20
    CONTENT_PADDING = 30
    MARGIN = 20
    
    # Border radius
    BORDER_RADIUS = 12
    CONTENT_BORDER_RADIUS = 8
    
    # Text Content
    TITLE = "End User License Agreement"
    SUBTITLE = "Please read the following terms carefully"
    
    # Section Headings
    TERMS_HEADING = "Terms of Use"
    ACCEPTANCE_HEADING = "Acceptance of Terms"
    DISCLAIMER_HEADING = "Important Disclaimers"
    
    # Button Labels
    AGREE_BUTTON = "Agree"
    DISAGREE_BUTTON = "Disagree"
    
    # Exit View Text
    EXIT_TITLE = "EULA Not Accepted"
    EXIT_MESSAGE = "You must agree to the EULA to use this application.\n\nPlease close the application manually."
    
    # Content Paragraphs
    TERMS_CONTENT = (
"This tool was created by the Science and Research Branch of the Ontario Ministry of Natural Resources (MNR). Use of this tool is governed by the terms and conditions set out below and implies acceptance of these terms."    )
    
    ACCEPTANCE_CONTENT = (
   "By clicking 'Agree,' you acknowledge that you have read, understood, and agree to be bound by all terms and conditions outlined in this agreement."
    )
    
    DISCLAIMER_CONTENT = (
      """This tool is made available by MNR as a public service on an “as is, with all defects” and “as available” basis, without any warranties, representations, or conditions of any kind, express or implied, arising by law or otherwise, including, without limitation, that the user’s use of this tool will be uninterrupted, that the operation of this tool will be error-free, or that this tool will meet the user’s requirements. \n\n MNR specifically disclaims any implied warranties or conditions of merchantable quality, fitness for a particular purpose, non-infringement of third-party rights, or those arising by law or by usage of trade or course of dealing. \n\n Use of this tool is at the user's sole risk, and the entire risk as to the results from, and performance of, this tool is assumed by the user. \n\n Under no circumstances will His Majesty the King in Right of Ontario or the members of the Executive Council and their employees, agents and independent contractors have any responsibility or liability for any loss, damage or injury whatsoever, regardless of cause, arising from access to, use of, inability to use, failure of, any errors or omissions in, or reliance on this tool (including, without limitation, direct, indirect, special, incidental, consequential, punitive, exemplary or other damages, and including, without limitation, any loss of profit, costs, expenses, harm to business or reputation, business interruption, loss of information or programs or data, loss of savings, loss of revenue, loss of goodwill, loss of tangible or intangible property, legal fees or legal costs, wasted management or office time or damages of any kind whatsoever), whether based in contract, tort, negligence or on any other legal basis, arising out of or in connection with the use of this tool, even if the Government of Ontario has been specifically advised of the possibility of such loss, damage or injury or if such loss, damage or injury was foreseeable."""


        
          )
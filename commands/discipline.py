from client_interactions import delete_message, send_message

DEMERIT_CNT         = 3
CITATION_CNT        = 5
VILOLATION_CNT      = 4
VERB_WARNING_CNT    = 3
WRITTEN_WARNING_CNT = 2

"""
Discipline command
Severely punishes the non elect
ex: !discipline josh
@param client: The discord client, generally assumed to be the bot user itself
@param message: The message the discord bot is responding to
@param name: Individual being shamed
@result: Deletes messages always
@result: Punishes always
@result: Gives report card always
"""
async def command( client, message, name ):
    await delete_message(message)
    
    send_message( message, "Message Deleted" )
    
    #Open the file, and unpack contents
    f = open( "discipline.txt", "r" )
    send_message( message, "File Opened" )
    data = unpack_file( f )
    send_message( message, "File Unpacked" )

    #Discipline the delinquent individual
    add_demerit( name, data )
    send_message( message, "Demerit Added" )

    #Re-pack the file contents, and write to the file
    f = open( "discipline.txt", "w" )
    send_message( message, "File Opened for writing" )
    pack_file( f, data ) 
    send_message( message, "File Packed and written" )
    
    evaluate( client, message, name )
    send_message( message, "Evaluation complete" )

async def evaluate( client, message, name ):
    await delete_message(message)
    
    #Open the file, and unpack contents
    f = open( "discipline.txt", "r" )
    data = unpack_file( f )

    
    i = locate_offender( name, data )
    report_card = create_report( name, data, i )

    send_message( message, report_card )
    
def add_demerit( name, data ):
    #Check for repeat offenders
    i = locate_offender( name, data )
    
    if( i == -1 or i == len( data ) ):
        #Process new hooligans
        data[ i + 1 ] = { 'name':name.upper(), 'count':1 }
    else:
        #Process repeat offenders
        data[ i ][ 'count' ] += 1

def create_report( name, data, i ):
    report = ""
    if( i == -1 or i == len( data ) ):
        report = name + " is squeaky clean."
    else:
        cnt = data[ i ][ 'count' ]

        #Calculate sinfulness
        demerit_cnt = cnt % DEMERIT_CNT
        citation_cnt = ( cnt // DEMERIT_CNT ) % CITATION_CNT
        violation_cnt = ( cnt // ( DEMERIT_CNT * CITATION_CNT ) ) % VILOLATION_CNT
        verb_warning_cnt = ( cnt // ( DEMERIT_CNT * CITATION_CNT * VILOLATION_CNT ) ) % VERB_WARNING_CNT
        written_warning_cnt = ( cnt // ( DEMERIT_CNT * CITATION_CNT * VILOLATION_CNT * VERB_WARNING_CNT ) ) % WRITTEN_WARNING_CNT
        disciplinary_review_cnt = cnt // ( DEMERIT_CNT * CITATION_CNT * VILOLATION_CNT * VERB_WARNING_CNT * WRITTEN_WARNING_CNT )

        #Create an exact report of how depraved you are
        report = "Demerits:" + str( demerit_cnt ) + "\n"
        report = report + "Citations: " + str( citation_cnt ) + "\n"
        report = report + "Violations: " + str( violation_cnt ) + "\n"
        report = report + "Verbal Warnings: " + str( verb_warning_cnt ) + "\n"
        report = report + "Written Warnings: " + str( written_warning_cnt ) + "\n"
        report = report + "Disciplinary Reviews: " + str( disciplinary_review_cnt ) + "\n"

    return report

def locate_offender( name, data ):
    #Get em
    if not data:
        i = -1
    else:
        for i in range( len( data ) ):
            if( data[ i ][ 'name' ] == name.upper() ):
                #Got em
                break

    #Return index
    return i

def unpack_file( f ):
    #Get the encrypted file text, and decrypt it
    data = {}
    encr_txt = f.read()
    file_txt = decrypt( 'QUADLINGS', encr_txt )

    #Convert the raw text into a name value pair
    lines = file_txt.split( '\n' )
    for i in range( len( lines ) - 1 ):
        line_data = lines[ i ].split( ' ' )
        data[ i ] = { 'name':line_data[ 0 ].upper(), 'count':int( line_data[ 1 ] ) }

    #Return the file data
    return data

def pack_file( f, data ):
    #Convert name value pairs into raw text
    raw_text = ""
    for i in range( len( data ) ):
        raw_text = raw_text + data[ i ][ 'name' ]
        raw_text = raw_text + " "
        raw_text = raw_text + str( data[ i ][ 'count' ] )
        raw_text = raw_text + "\n"

    #Encrypt the text, and write it to a file
    encr_txt = encrypt( 'QUADLINGS', raw_text )
    f.write( encr_txt )

def encrypt( key, string ):
    #Protec da file
    encoded_chars = []
    for i in range( len( string ) ):
        key_c = key[ i % len( key ) ]
        encoded_c = chr( ( ord( string[ i ] ) + ord( key_c ) ) % 256 )
        encoded_chars.append( encoded_c )
        
    encoded_string = "".join( encoded_chars )
    return encoded_string

def decrypt( key, string ):
    #Un-protec the file
    decoded_chars = []
    for i in range( len( string ) ):
        key_c = key[ i % len( key ) ]
        decoded_c = chr( ( ord( string[ i ] ) - ord( key_c ) ) % 256 )
        decoded_chars.append( decoded_c )
        
    decoded_string = "".join( decoded_chars )
    return decoded_string
    
# String that triggers this command
TRIGGER = '!discipline'

def is_triggered(message_content):
  return message_content.lower() == TRIGGER

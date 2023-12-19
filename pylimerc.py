class PyLimeRc:

    def __init__(self, url=None):
        self.headers = {'content-type': 'application/json',
                        'connection': 'Keep-Alive'}
        self.url = url
        self.session_key = None

    def set_headers(self, headers):
        self.headers = headers

    def set_url(self, url):
        self.url = url

    def __sort_params(self, method, params):
        import yaml

        config = yaml.safe_load(open('pylimerc.yml'))
        sorted_params = []
        if self.session_key is not None:
            sorted_params.append(self.session_key)

        if method not in config['lime_methods']:
            return params.values()

        sequence = config['lime_methods'][method]
        for s in sequence:
            param = params.get(s)
            if param:
                sorted_params.append(param)
            else:
                return sorted_params
        return sorted_params

    def __format_params(self, params):
        del params['self']
        params['sSessionKey'] = self.session_key
        return dict((k, v) for k, v in params.items() if v is not None)

    def call_rpc(self, method, params):
        """
          Generic call. This routine makes a request to the rpc directly. Its provide more control to the user.
          Moreover, this routine permits evoke new RPC's methods not implemented in this class.
          More information about the RPC's methods, see: http://api.limesurvey.org/classes/remotecontrol_handle.html

          Args:
                method (str): The name of the RPC's method
                params (list): a list of parameters that is required by the method

            Returns:
                list: The result of the activation
        """
        import requests
        import sys

        print("Method: %s" % method)
        print("Params before: %s" % params)
        params = self.__sort_params(method, params)
        print("Params sorted: %s" % params)

        payload = {"method": method, "params": params, "id": 1}
        try:
            r = requests.post(url=self.url, headers=self.headers, json=payload)
            return r
        except:
            ex = sys.exc_info()[0]
            print("Exception: %s" % ex)
        return

    def get_session_key(self, username, password):
        """
            RPC routine to create a session key.
            Using this function you can create a new XML/JSON-RPC session key.
            This is mandatory for all following LSRC2 function calls.
            Args:
                username (str): username
                password (str): password
            Returns:
                string: The session key. Each instance keeps the session key internally.
        """
        params = self.__format_params(locals().copy())
        method = "get_session_key"
        r = self.call_rpc(method, params)
        if type(r.json()['result']) is not dict:
            self.session_key = r.json()['result']
        return self.session_key

    def get_site_settings(self, sSettingName):
        """
        RPC Routine to get settings.

        Args:
            sSettingName (str): Name of the setting to get
        Returns:
            string: The requested value
        """
        params = self.__format_params(locals().copy())
        method = "get_site_settings"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_summary(self, iSurveyID, sStatName=None):
        """
            RPC routine to get survey summary, regarding token usage and survey participation.
            Returns the requested value as string.

            Args:
                iSurveyID (int): Id of the Survey to get summary
                sStatName (:obj:`str`, optional): Name of the summary - valid values are 'token_count', 'token_invalid', 'token_sent', 'token_opted_out', 'token_completed', 'completed_responses', 'incomplete_responses', 'full_responses' or 'all'
            Returns:
                string: The requested value or an list of all values when sStatName = 'all'
        """
        params = self.__format_params(locals().copy())
        method = "get_summary"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_survey_properties(self, iSurveyID, aSurveySettings):
        """
            RPC Routine to get survey properties.

            Args:
                iSurveyID (int): The id of the Survey to be checked
                aSurveySettings (list): The properties to get
            Returns:
                list: list with the properties
        """
        params = self.__format_params(locals().copy())
        method = "get_survey_properties"
        print
        params
        r = self.call_rpc(method, params)
        return r.json()['result']

    def import_group(self, iSurveyID, sImportData, sImportDataType,
                     sNewGroupName=None, sNewGroupDescription=None):
        """
            RPC Routine to import a group - imports lsg,csv

            Args:
                iSurveyID (int): The id of the survey that the group will belong
                sImportData (str): containing the BASE 64 encoded data of a lsg,csv
                sImportDataType (str): lsg,csv
                sNewGroupName (:obj:`str`, optional): New name for the group
                sNewGroupDescription (:obj:`str`, optional): New description for the group
            Returns:
                list|int: iGroupID - ID of the new group or status
        """
        params = self.__format_params(locals().copy())
        method = "import_group"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def import_survey(self, sImportData, sImportDataType, sNewSurveyName=None, DestSurveyID=None):
        """
            RPC Routine to import a survey - imports lss,csv,xls or survey zip archive.

            Args:
                sImportData (str): String containing the BASE 64 encoded data of a lss,csv,xls or survey zip archive
                sImportDataType (str): lss,csv,txt or zip
                sNewSurveyName (:obj:`str`, optional): The optional new name of the survey
                DestSurveyID (:obj:`int`, optional) This is the new ID of the survey - if already used a random one will be taken instead
            Returns:
                list|integer: iSurveyID - ID of the new survey
        """
        params = self.__format_params(locals().copy())
        method = "import_survey"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def list_groups(self, iSurveyID):
        """
            RPC Routine to return the ids and info of groups belonging to survey .
            Returns list of ids and info.

            Args:
                iSurveyID (int): Id of the Survey containing the groups
            Returns:
                list: The list of groups
        """
        params = self.__format_params(locals().copy())
        method = "list_groups"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def list_participants(self, iSurveyID, iStart, iLimit, bUnused, aAttributes, aConditions=None):
        """
            RPC Routine to return the ids and info of token/participants of a survey.
            if $bUnused is true, user will get the list of not completed tokens (token_return functionality).
            Parameters iStart and ilimit are used to limit the number of results of this call.
            Parameter aAttributes is an optional list containing more attribute that may be requested

            Args:
                iSurveyID (int): Id of the survey to list participants
                iStart (int): Start id of the token list
                iLimit (int): Number of participants to return
                bUnused (bool): If you want unused tokens, set true
                aAttributes (bool|list): The extented attributes that we want
                aConditions (:obj:`list`, optional): Optional conditions to limit the list, e.g. with list('email':'info@example.com')
            Returns:
                list: The list of tokens
        """
        params = self.__format_params(locals().copy())
        method = "list_participants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def list_surveys(self, sUser=None):
        """
            RPC Routine to list the ids and info of surveys belonging to a user.
            Returns list of ids and info.
            If user is admin he can get surveys of every user (parameter sUser) or all surveys (sUser=null)
            Else only the syrveys belonging to the user requesting will be shown.

            Args:
                sUser (:obj:`str`, optional) Optional username to get list of surveys
            Returns:
                list: The list of surveys
        """
        params = self.__format_params(locals().copy())
        method = "list_surveys"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def release_session_key(self):
        """
            Closes the RPC session
            Returns:
                   Return a string with the status.
        """
        if self.session_key:
            params = self.__format_params(locals().copy())
            method = "release_session_key"
            r = self.call_rpc(method, params)
            if r.json()['result'] == 'OK':
                self.session_key = None
        return

    def activate_survey(self, iSurveyID):
        """
          RPC Routine that launches a newly created survey. (Access public)

          Args:
                iSurveyID (int): $iSurveyID The id of the survey to be activated

            Returns:
                list: The result of the activation
        """
        params = self.__format_params(locals().copy())
        method = "activate_survey"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def list_users(self):
        """
            RPC Routine to list the ids and info of users.
            Returns list of ids and info.
            Returns:
                list: The list of users
        """
        params = self.__format_params(locals().copy())
        method = "list_users"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def list_questions(self, iSurveyID, iGroupID=None, sLanguage=None):
        """
            RPC Routine to return the ids and info of (sub-)questions of a survey/group.
            Returns list of ids and info.

            Args:
                iSurveyID (int): Id of the survey to list questions
                iGroupID (:obj:`int`, optional): Optional id of the group to list questions
                sLanguage (:obj:`str`, optional): Optional parameter language for multilingual questions
            Returns:
                list: The list of questions
        """
        params = self.__format_params(locals().copy())
        method = "list_questions"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def import_question(self, iSurveyID, iGroupID, sImportData, sImportDataType,
                        sMandatory=None, sNewQuestionTitle=None, sNewqQuestion=None,
                        sNewQuestionHelp=None):
        """
            RPC Routine to import a question - imports lsq,csv.

            Args:
                iSurveyID (int): The id of the survey that the question will belong
                iGroupID (int): The id of the group that the question will belong
                sImportData (str): String containing the BASE 64 encoded data of a lsg,csv
                sImportDataType (str): lsq,csv
                sMandatory (:obj:`str`, optional): Mandatory question option (default to No)
                sNewQuestionTitle (:obj:`str`, optional): Optional new title for the question
                sNewqQuestion (:obj:`str`, optional): An optional new question
                sNewQuestionHelp (:obj:`str`, optional): An optional new question help text
            Returns:
                list|integer: iQuestionID - ID of the new question - Or status
        """
        params = self.__format_params(locals().copy())
        method = "import_question"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def invite_participants(self, iSurveyID):
        """
            RPC Routine to invite participants in a survey
            Returns list of results of sending

            Args:
            iSurveyID (int): ID of the survey that participants belong
            Returns:
                list: Result of the action
        """
        params = self.__format_params(locals().copy())
        method = "invite_participants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def mail_registered_participants(self, iSurveyID, overrideAllConditions):
        """
            RPC Routine to send register mails to participants in a survey
            Returns list of results of sending

            Args:
            iSurveyID (int): ID of the survey that participants belong
            overrideAllConditions (list): Replace the default conditions, like this:
                * overrideAllConditions = list(self);
                * overrideAllConditions[] = 'tid = 2';
                * response = $myJSONRPCClient->mail_registered_participants( $sessionKey, $survey_id, $overrideAllConditions );
            Returns:
                list: Result of the action
        """
        params = self.__format_params(locals().copy())
        method = "mail_registered_participants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def activate_tokens(self, iSurveyID, aAttributeFields):
        """
            RPC routine to to initialise the survey's collection of tokens where new participant tokens may be later added.

            Args:
                iSurveyID (int): ID of the survey where a token table will be created for
                aAttributeFields (int): An list of integer describing any additional attribute fields
            Returns:
                list: Status=>OK when successfull, otherwise the error description
        """
        params = self.__format_params(locals().copy())
        method = "activate_tokens"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def add_group(self, iSurveyID, sGroupTitle, sGroupDescription=None):
        """
            RPC Routine to add an empty group with minimum details.
            Used as a placeholder for importing questions.
            Returns the groupid of the created group.

            Args:
                iSurveyID (int): Dd of the Survey to add the group
                sGroupTitle (str): Name of the group
                sGroupDescription (:obj:`str`,optional): Optional description of the group
            Returns:
                list|int: The id of the new group - Or status
        """
        params = self.__format_params(locals().copy())
        method = "add_group"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def add_language(self, iSurveyID, sLanguage):
        """
            RPC Routine to add a survey language.

            Args:
                iSurveyID (int): ID of the survey where a token table will be created for
                sLanguage (str): A valid language shortcut to add to the current survey. If the language already exists no error will be given.
            Returns:
                list: Status=>OK when successfull, otherwise the error description
        """
        params = self.__format_params(locals().copy())
        method = "add_language"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def add_participants(self, iSurveyID, aParticipantData, bCreateToken=None):
        """
            RPC Routine to add participants to the tokens collection of the survey.
            Returns the inserted data including additional new information like the Token entry ID and the token string.

            Args:
                iSurveyID (int): Id of the Survey
                aParticipantData (dict): Data of the participants to be added
                bCreateToken (:obj:`bool`,optional): Optional - Defaults to true (rpc side) and determins if the access token automatically created
                Returns:
                    list: The values added
        """
        params = self.__format_params(locals().copy())
        method = "add_participants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def add_response(self, iSurveyID, aResponseData):
        """
            RPC Routine to add a response to the survey responses collection.
            Returns the id of the inserted survey response

            Args:
                iSurveyID (int): Id of the Survey to insert responses
                aResponseData (dict): The actual response
            Returns:
                int: The response ID
        """
        params = self.__format_params(locals().copy())
        method = "add_response"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def add_survey(self, iSurveyID, sSurveyTitle, sSurveyLanguage, sformat):
        """
            RPC Routine to add an empty survey with minimum details.
            Used as a placeholder for importing groups and/or questions.

            Args:
                iSurveyID (int): The wish id of the Survey to add
                sSurveyTitle (str): Title of the new Survey
                sSurveyLanguage (str): Default language of the Survey
                sformat (str): Question appearance format
            Returns:
                list|string|int: return values (not described at RPC Api documentation)
        """
        params = self.__format_params(locals().copy())
        method = "add_survey"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def cpd_importParticipants(self, aParticipants):
        """
            This function import a participant to the LimeSurvey cpd. It stores attributes as well, if they are registered before within ui

            Args:
                aParticipants (list): [[0] => ["email"=>"dummy-02222@limesurvey.com","firstname"=>"max","lastname"=>"mustermann"]]
            Returns:
                list: List with status
        """
        params = self.__format_params(locals().copy())
        method = "cpd_importParticipants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def delete_group(self, iSurveyID, iGroupID):
        """
            RPC Routine to delete a group of a survey .
            Returns the id of the deleted group.

            Args:
                iSurveyID (int): Id of the survey that the group belongs
                iGroupID (int): Id of the group to delete
            Returns:
                list|int: The id of the deleted group or status
        """
        params = self.__format_params(locals().copy())
        method = "delete_group"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def delete_language(self, iSurveyID, sLanguage):
        """
            RPC Routine to delete a survey language.

            Args:
                iSurveyID (int): ID of the survey where a token table will be created for
                sLanguage (str): A valid language shortcut to delete from the current survey. If the language does not exist in that survey no error will be given.
            Returns:
                list: Status=>OK when successfull, otherwise the error description
            """
        params = self.__format_params(locals().copy())
        method = "delete_language"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def delete_participants(self, iSurveyID, aTokenIDs):
        """
            RPC Routine to delete multiple participants of a Survey.
            Returns the id of the deleted token

            Args:
                iSurveyID (int): Id of the Survey that the participants belong to
                aTokenIDs (list): Id of the tokens/participants to delete
            Returns:
                list: Result of deletion
        """
        params = self.__format_params(locals().copy())
        method = "delete_participants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def delete_question(self, iQuestionID):
        """
            RPC Routine to delete a question of a survey .
            Returns the id of the deleted question.

            Args:
                iQuestionID (int): Id of the question to delete
            Returns:
                list|int: Id of the deleted Question or status
        """
        params = self.__format_params(locals().copy())
        method = "delete_question"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def delete_survey(self, iSurveyID):
        """
            RPC Routine to delete a survey.

            Args:
                iSurveyID (int): The id of the Survey to be deleted
            Returns:
                list: Returns Status
        """
        params = self.__format_params(locals().copy())
        method = "delete_survey"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def export_responses(self, iSurveyID, sDocumentType, sLanguageCode,
                         sCompletionStatus=None, sHeadingType=None, sResponseType=None,
                         iFromResponseID=None, iToResponseID=None, aFields=None):
        """
            RPC Routine to export responses.
            Returns the requested file as base64 encoded string

            Args:
                iSurveyID (int): Id of the Survey
                sDocumentType (str): pdf,csv,xls,doc,json
                sLanguageCode (str): The language to be used
                sCompletionStatus (:obj:`str`,optional): Optional 'complete','incomplete' or 'all' - defaults to 'all'
                sHeadingType (:obj:`str`,optional): 'code','full' or 'abbreviated' Optional defaults to 'code'
                sResponseType (:obj:`str`,optional): 'short' or 'long' Optional defaults to 'short'
                iFromResponseID (:obj:`int`,optional): Optional
                iToResponseID (:obj:`int`,optional): Optional
                        aFields (:obj:`list`,optional) Optional Selected fields
            Returns:
                list|string: On success: Requested file as base 64-encoded string. On failure list with error information
        """
        params = self.__format_params(locals().copy())
        method = "export_responses"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def export_responses_by_token(self, iSurveyID, sDocumentType, sToken, sLanguageCode,
                                  sCompletionStatus=None, sHeadingType=None, sResponseType=None, aFields=None):
        """
            RPC Routine to export token response in a survey.
            Returns the requested file as base64 encoded string

            Args:
                iSurveyID (int): Id of the Survey
                sDocumentType (str): pdf,csv,xls,doc,json
                sToken (str): The token for which responses needed
                sLanguageCode (str): The language to be used
                sCompletionStatus (:obj:`str`,optional): Optional 'complete','incomplete' or 'all' - defaults to 'all'
                sHeadingType (:obj:`str`,optional): 'code','full' or 'abbreviated' Optional defaults to 'code'
                sResponseType (:obj:`str`,optional): 'short' or 'long' Optional defaults to 'short'
                        aFields (:obj:`list`,optional) Optional Selected fields
            Returns:
                list|string: On success: Requested file as base 64-encoded string. On failure list with error information
        """
        params = self.__format_params(locals().copy())
        method = "export_responses_by_token"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def export_statistics(self, iSurveyID, docType,
                          sLanguage=None, graph=None, groupIDs=None):
        """
            RPC routine to export statistics of a survey to a user.
            Returns string - base64 encoding of the statistics.

            Args:
                iSurveyID (int): Id of the Survey
                docType (str): Type of documents the exported statistics should be
                sLanguage (:obj:`str`,optional): Optional language of the survey to use
                graph (:obj:`str`,optional): Create graph option
                groupIDs (int|list,optional): An OPTIONAL list (ot a single int) containing the groups we choose to generate statistics from
            Returns:
                string: Base64 encoded string with the statistics file
        """
        params = self.__format_params(locals().copy())
        method = "export_statistics"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def export_timeline(self, iSurveyID, sType, dStart, dEnd):
        """
            RPC Routine to export submission timeline.
            Returns an list of values (count and period)

            Args:
                iSurveyID (int): Id of the Survey
                sType (str): (day|hour)
                dStart (str): start
                dEnd (str): end
            Returns:
                list: On success: The timeline. On failure list with error information
        """
        params = self.__format_params(locals().copy())
        method = "export_timeline"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_group_properties(self, iGroupID, aGroupSettings):
        """
            RPC Routine to return properties of a group of a survey .
            Returns list of properties

            Args:
                iGroupID (int): Id of the group to get properties
                aGroupSettings (list): The properties to get
            Returns:
                list: The requested values
        """
        params = self.__format_params(locals().copy())
        method = "get_group_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_language_properties(self, iSurveyID, aSurveyLocaleSettings, sLang):
        """
            RPC Routine to get survey language properties.

            Args:
                iSurveyID (int): Dd of the Survey
                aSurveyLocaleSettings (list): Properties to get
                sLang (str): Language to use
            Returns:
                list: The requested values
        """
        params = self.__format_params(locals().copy())
        method = "get_language_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_participant_properties(self, iSurveyID, iTokenID, aTokenProperties):
        """
            RPC Routine to return settings of a token/participant of a survey .

            Args:
                iSurveyID (int): Id of the Survey to get token properties
                iTokenID (int): Id of the participant to check
                aTokenProperties (list): The properties to get
            Returns:
                list: The requested values
        """
        params = self.__format_params(locals().copy())
        method = "get_participant_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_question_properties(self, iQuestionID, aQuestionSettings, sLanguage=None):
        """
            RPC Routine to return properties of a question of a survey.
            Returns string

            Args:
                iQuestionID (int): Id of the question to get properties
                aQuestionSettings (list): The properties to get
                sLanguage (:obj:`str`,optional): Optional parameter language for multilingual questions
            Returns:
                list: The requested values
        """
        params = self.__format_params(locals().copy())
        method = "get_question_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def get_response_ids(self, iSurveyID, sToken):
        """
            RPC Routine to find response IDs given a survey ID and a token.
            Args:
                iSurveyID (int): ID of the survey
                sToken (str): The token for which responses needed
        """
        params = self.__format_params(locals().copy())
        method = "get_response_ids"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def remind_participants(self, iSurveyID, iMinDaysBetween=None, iMaxReminders=None):
        """
            RPC Routine to send reminder for participants in a survey
            Returns list of results of sending

            Args:
                iSurveyID (int): ID of the survey that participants belong
                iMinDaysBetween (:obj:`int`,optional): Optional parameter days from last reminder
                iMaxReminders (:obj:`int`,optional): Optional parameter Maximum reminders count
            Returns:
                list: Result of the action
        """
        params = self.__format_params(locals().copy())
        method = "remind_participants"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def set_group_properties(self, iGroupID, aGroupData):
        """
            RPC Routine to set group properties.

            Args:
                iGroupID (int): ID of the survey
                aGroupData (dict): A list with the particular fieldnames as keys and their values to set on that particular survey
            Returns:
                list: Of succeeded and failed modifications according to internal validation.
        """
        params = self.__format_params(locals().copy())
        method = "set_group_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def set_language_properties(self, iSurveyID, aSurveyLocaleData, sLanguage=None):
        """
            RPC Routine to set survey language properties.

            Args:
                iSurveyID (int): - ID of the survey
                aSurveyLocaleData (dict): An list with the particular fieldnames as keys and their values to set on that particular survey
                sLanguage (:obj:`str`,optional): Optional - Language to update - if not give the base language of the particular survey is used
            Returns:
                list: Status=>OK, when save successful otherwise error text.
        """
        params = self.__format_params(locals().copy())
        method = "set_language_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def set_participant_properties(self, iSurveyID, iTokenID, aTokenData):
        """
            RPC Routine to set properties of a survey participant/token.
            Returns list

            Args:
                iSurveyID (int): Id of the survey that participants belong
                iTokenID (int): Id of the participant to alter
                aTokenData (list|dict) Data to change
            Returns:
                list: Result of the change action
        """
        params = self.__format_params(locals().copy())
        method = "set_participant_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def set_question_properties(self, iQuestionID, aQuestionData, sLanguage=None):
        """
            RPC Routine to set question properties.

            Args:
                iQuestionID (int): ID of the question
                aQuestionData (list|dict): A list with the particular fieldnames as keys and their values to set on that particular question
                sLanguage (:obj:`str`,optional): Optional parameter language for multilingual questions
            Returns:
                list: List of succeeded and failed modifications according to internal validation.
        """
        params = self.__format_params(locals().copy())
        method = "set_question_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def set_survey_properties(self, iSurveyID, aSurveyData):
        """
            RPC Routine to set survey properties.

            Args:
                iSurveyID (int): ID of the survey
                aSurveyData (list|dict): A list with the particular fieldnames as keys and their values to set on that particular survey
            Returns:
                list: List of succeeded and failed nodifications according to internal validation.
        """
        params = self.__format_params(locals().copy())
        method = "set_survey_properties"
        r = self.call_rpc(method, params)
        return r.json()['result']

    def update_response(self, iSurveyID, aResponseData):
        """
            RPC Routine to update a response in a given survey.
            Routine supports only single response updates.
            Response to update will be identified either by the response id, or the token if response id is missing.
            Routine is only applicable for active surveys with alloweditaftercompletion = Y.

            Args:
                iSurveyID (int): Id of the Survey to update response
                aResponseData (dict): The actual response
            Returns:
                bool|str: True on success. errormessage on error
        """
        params = self.__format_params(locals().copy())
        method = "update_response"
        r = self.call_rpc(method, params)
        return r.json()['result']

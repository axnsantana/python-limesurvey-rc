class PyLimeRc:

    def __init__(self,url=None):
        self.headers = {'content-type':'application/json',
               'connection':'Keep-Alive'}
        self.url=url
        self.session_key=None


    def set_url(self,url):
        self.url=url

    def call_rpc(self,method,params):
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
        payload = {"method":method,"params":params,"id":1}
        try:
           r = requests.post(url=self.url, headers=self.headers, json=payload)
           return r
        except :
            ex = sys.exc_info()[0]
            print ( "Exception: %s" % ex)
        return

    def get_session_key(self,username,password):
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
        params = {'username':username, 'password':password}
        method = "get_session_key"
        r = self.call_rpc(method,params)
        self.session_key = r.json()['result'];
        return self.session_key;

    def get_site_settings(self, sSettingName):
        """
        RPC Routine to get settings.

        Args:
            sSettingName (str): Name of the setting to get
        Returns:
            string: The requested value
        """
        method = "get_site_settings"
        params = {'sSessionKey':self.session_key,'sSettingName':sSettingName}
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def get_summary(self,iSurveyID,sStatName=None):
        """
            RPC routine to get survey summary, regarding token usage and survey participation.
            Returns the requested value as string.

            Args:
                iSurveyID (int): Id of the Survey to get summary
                sStatName (:obj:`str`, optional): Name of the summary - valid values are 'token_count', 'token_invalid', 'token_sent', 'token_opted_out', 'token_completed', 'completed_responses', 'incomplete_responses', 'full_responses' or 'all'
            Returns:
                string: The requested value or an list of all values when sStatName = 'all'
        """
        method = "get_summary"
        params = {'sSessionKey':self.session_key,'iSurveyID':iSurveyID}
        if sStatName is not None:
            params['sStatName'] = sStatName
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def get_survey_properties(self,iSurveyID,aSurveySettings):
        """
            RPC Routine to get survey properties.

            Args:
                iSurveyID (int): The id of the Survey to be checked
                aSurveySettings (list): The properties to get
            Returns:
                list: list with the properties
        """
        method = "get_survey_properties"
        params = {'sSessionKey':self.session_key,'iSurveyID':iSurveyID,'aSurveySettings':aSurveySettings}
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def import_group(self,iSurveyID,sImportData,sImportDataType,
                     sNewGroupName=None,sNewGroupDescription=None):
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
        method = "import_group"
        params = {'sSessionKey':self.session_key,'iSurveyID':iSurveyID,
                  'sImportData':sImportData,'sImportDataType':sImportDataType}
        if sNewGroupName is not None:
            params[sNewGroupName] = sNewGroupName
        if sNewGroupDescription is not None:
            params[sNewGroupDescription] = sNewGroupDescription
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def import_survey(self,sImportData,sImportDataType,sNewSurveyName=None,DestSurveyID=None):
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
        method = "import_survey"
        params = {'sSessionKey':self.session_key,'sImportData':sImportData,'sImportDataType':sImportDataType}
        if sNewSurveyName is not None:
            params['sNewSurveyName'] = sNewSurveyName
        if DestSurveyID is not None:
            params['DestSurveyID'] = DestSurveyID
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def list_groups(self,iSurveyID):
        """
            RPC Routine to return the ids and info of groups belonging to survey .
            Returns list of ids and info.

            Args:
                iSurveyID (int): Id of the Survey containing the groups
            Returns:
                list: The list of groups
        """
        method = "list_groups"
        params = {'sSessionKey':self.session_key,'iSurveyID':iSurveyID}
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def list_participants(self,iSurveyID,iStart,iLimit,bUnused,aAttributes,aConditions=None):
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
        method = "list_participants"
        params = {'sSessionKey':self.session_key,'iSurveyID':iSurveyID,
                  'iStart':iStart,'iLimit':iLimit,
                  'bUnused':bUnused,'aAttributes':aAttributes}
        if aConditions is not None:
            params['aConditions'] = aConditions
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def list_surveys(self,sUser=None):
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
        method = "list_surveys"
        params = {'sSessionKey':self.session_key}
        if sUser is not None:
            params['sUser'] = sUser
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def release_session_key(self):
        """
            Closes the RPC session
            Returns:
                   Return a string with the status.
        """
        method = "release_session_key"
        params = {'sSessionKey':self.session_key}
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def activate_survey(self,iSurveyID):
        """
          RPC Routine that launches a newly created survey. (Access public)

          Args:
                iSurveyID (int): $iSurveyID The id of the survey to be activated

            Returns:
                list: The result of the activation
        """
        method = "activate_survey"
        params = {'sSessionKey':self.session_key, 'iSurveyID':iSurveyID}
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def list_users(self):
        """
            RPC Routine to list the ids and info of users.
            Returns list of ids and info.
            Returns:
                list: The list of users
        """
        method = "list_users"
        params = {'sSessionKey':self.session_key}
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def list_questions(self, iSurveyID, iGroupID,  sLanguage):
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
        method = "list_questions"
        params = {'sSessionKey':self.session_key, 'iSurveyID':iSurveyID}
        if iGroupID is not None:
            params['iGroupID'] = iGroupID
        if sLanguage is not None:
            params['sLanguage'] = sLanguage
        r = self.call_rpc(method,params)
        return r.json()['result'];

    def import_question(self):
        return;
    """
    * RPC Routine to import a question - imports lsq,csv.
    *
    * @access public
    * @param string $sSessionKey
    * @param int $iSurveyID The id of the survey that the question will belong
    * @param int $iGroupID The id of the group that the question will belong
    * @param string $sImportData String containing the BASE 64 encoded data of a lsg,csv
    * @param string $sImportDataType lsq,csv
    * @param string $sMandatory Optional Mandatory question option (default to No)
    * @param string $sNewQuestionTitle Optional new title for the question
    * @param string $sNewqQuestion An optional new question
    * @param string $sNewQuestionHelp An optional new question help text
    * @return list|integer iQuestionID - ID of the new question - Or status
    """

    def invite_participants(self):
        return;
    """
    * RPC Routine to invite participants in a survey
    * Returns list of results of sending
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID ID of the survey that participants belong
    * @return list Result of the action
    """

    def mail_registered_participants(self):
        return;
    """
    * RPC Routine to send register mails to participants in a survey
    * Returns list of results of sending
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID ID of the survey that participants belong
    * @param list $overrideAllConditions replace the default conditions, like this:
    * $overrideAllConditions = list(self);
    * $overrideAllConditions[] = 'tid = 2';
    * $response = $myJSONRPCClient->mail_registered_participants( $sessionKey, $survey_id, $overrideAllConditions );
    * @return list Result of the action
    """

    def activate_tokens(self):
        return;
    """
    * RPC routine to to initialise the survey's collection of tokens where new participant tokens may be later added.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iSurveyID ID of the survey where a token table will be created for
    * @param list $aAttributeFields An list of integer describing any additional attribute fields
    * @return list Status=>OK when successfull, otherwise the error description
    """
    def add_group(self):
        return;
    """
    * RPC Routine to add an empty group with minimum details.
    * Used as a placeholder for importing questions.
    * Returns the groupid of the created group.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Dd of the Survey to add the group
    * @param string $sGroupTitle Name of the group
    * @param string $sGroupDescription Optional description of the group
    * @return list|int The id of the new group - Or status
    """
    def add_language(self):
        return;
    """
    * RPC Routine to add a survey language.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iSurveyID ID of the survey where a token table will be created for
    * @param string $sLanguage A valid language shortcut to add to the current survey. If the language already exists no error will be given.
    * @return list Status=>OK when successfull, otherwise the error description
    """
    def add_participants(self):
        return;
    """
    * RPC Routine to add participants to the tokens collection of the survey.
    * Returns the inserted data including additional new information like the Token entry ID and the token string.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey
    * @param struct $aParticipantData Data of the participants to be added
    * @param bool Optional - Defaults to true and determins if the access token automatically created
    * @return list The values added
    """
    def add_response(self):
        return;
    """
    * RPC Routine to add a response to the survey responses collection.
    * Returns the id of the inserted survey response
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey to insert responses
    * @param struct $aResponseData The actual response
    * @return int The response ID
    """
    def add_survey(self):
        return;
    """
    * RPC Routine to add an empty survey with minimum details.
    * Used as a placeholder for importing groups and/or questions.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID The wish id of the Survey to add
    * @param string $sSurveyTitle Title of the new Survey
    * @param string $sSurveyLanguage Default language of the Survey
    * @param string $sformat Question appearance format
    * @return list|string|int
    """
    def cpd_importParticipants(self):
        return;
    """
    * This function import a participant to the LimeSurvey cpd. It stores attributes as well, if they are registered before within ui
    *
    * Call the function with $response = $myJSONRPCClient->cpd_importParticipants( $sessionKey, $aParticipants);
    *
    * @param int $sSessionKey
    * @param list $aParticipants
    * [[0] => ["email"=>"dummy-02222@limesurvey.com","firstname"=>"max","lastname"=>"mustermann"]]
    * @return list with status
    """
    def delete_group(self):
        return;
    """
    * RPC Routine to delete a group of a survey .
    * Returns the id of the deleted group.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the survey that the group belongs
    * @param int $iGroupID Id of the group to delete
    * @return list|int The id of the deleted group or status
    """
    def delete_language(self):
        return;
    """
    * RPC Routine to delete a survey language.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iSurveyID ID of the survey where a token table will be created for
    * @param string $sLanguage A valid language shortcut to delete from the current survey. If the language does not exist in that survey no error will be given.
    * @return list Status=>OK when successfull, otherwise the error description
    """
    def delete_participants(self):
        return;
    """
    * RPC Routine to delete multiple participants of a Survey.
    * Returns the id of the deleted token
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey that the participants belong to
    * @param list $aTokenIDs Id of the tokens/participants to delete
    * @return list Result of deletion
    """
    def delete_question(self):
        return;
    """
    * RPC Routine to delete a question of a survey .
    * Returns the id of the deleted question.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int iQuestionID Id of the question to delete
    * @return list|int Id of the deleted Question or status
    """
    def delete_survey(self):
        return;
    """
    * RPC Routine to delete a survey.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID The id of the Survey to be deleted
    * @return list Returns Status
    """
    def export_responses(self):
        return;
    """
    * RPC Routine to export responses.
    * Returns the requested file as base64 encoded string
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey
    * @param string $sDocumentType pdf,csv,xls,doc,json
    * @param string $sLanguageCode The language to be used
    * @param string $sCompletionStatus Optional 'complete','incomplete' or 'all' - defaults to 'all'
    * @param string $sHeadingType 'code','full' or 'abbreviated' Optional defaults to 'code'
    * @param string $sResponseType 'short' or 'long' Optional defaults to 'short'
    * @param integer $iFromResponseID Optional
    * @param integer $iToResponseID Optional
    * @param list $aFields Optional Selected fields
    * @return list|string On success: Requested file as base 64-encoded string. On failure list with error information
    * """
    def export_responses_by_token(self):
        return;
    """
    * RPC Routine to export token response in a survey.
    * Returns the requested file as base64 encoded string
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey
    * @param string $sDocumentType pdf,csv,xls,doc,json
    * @param string $sToken The token for which responses needed
    * @param string $sLanguageCode The language to be used
    * @param string $sCompletionStatus Optional 'complete','incomplete' or 'all' - defaults to 'all'
    * @param string $sHeadingType 'code','full' or 'abbreviated' Optional defaults to 'code'
    * @param string $sResponseType 'short' or 'long' Optional defaults to 'short'
    * @param list $aFields Optional Selected fields
    * @return list|string On success: Requested file as base 64-encoded string. On failure list with error information
    *
    """
    def export_statistics(self):
        return;
    """
    * RPC routine to export statistics of a survey to a user.
    * Returns string - base64 encoding of the statistics.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey
    * @param string $docType Type of documents the exported statistics should be
    * @param string $sLanguage Optional language of the survey to use
    * @param string $graph Create graph option
    * @param int|list $groupIDs An OPTIONAL list (ot a single int) containing the groups we choose to generate statistics from
    * @return string Base64 encoded string with the statistics file
    """
    def export_timeline(self):
        return;
    """
    * RPC Routine to export submission timeline.
    * Returns an list of values (count and period)
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey
    * @param string $sType (day|hour)
    * @param string $dStart
    * @param string $dEnd
    * @return list On success: The timeline. On failure list with error information
    * """
    def get_group_properties(self):
        return;
    """
    * RPC Routine to return properties of a group of a survey .
    * Returns list of properties
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iGroupID Id of the group to get properties
    * @param list $aGroupSettings The properties to get
    * @return list The requested values
    """
    def get_language_properties(self):
        return;
    """
    * RPC Routine to get survey language properties.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Dd of the Survey
    * @param list $aSurveyLocaleSettings Properties to get
    * @param string $sLang Language to use
    * @return list The requested values
    """
    def get_participant_properties(self):
        return;
    """
    * RPC Routine to return settings of a token/participant of a survey .
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey to get token properties
    * @param int $iTokenID Id of the participant to check
    * @param list $aTokenProperties The properties to get
    * @return list The requested values
    """
    def get_question_properties(self):
        return;
    """
    * RPC Routine to return properties of a question of a survey.
    * Returns string
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iQuestionID Id of the question to get properties
    * @param list $aQuestionSettings The properties to get
    * @param string $sLanguage Optional parameter language for multilingual questions
    * @return list The requested values
    """
    def get_response_ids(self):
        return;
    """
    * RPC Routine to find response IDs given a survey ID and a token.
    * @param string $sSessionKey
    * @param int $iSurveyID
    * @param string $sToken
    """

    def remind_participants(self):
        return;
    """
    * RPC Routine to send reminder for participants in a survey
    * Returns list of results of sending
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID ID of the survey that participants belong
    * @param int $iMinDaysBetween Optional parameter days from last reminder
    * @param int $iMaxReminders Optional parameter Maximum reminders count
    * @return list Result of the action
    """
    def set_group_properties(self):
        return;
    """
    * RPC Routine to set group properties.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iGroupID - ID of the survey
    * @param list|struct $aGroupData - An list with the particular fieldnames as keys and their values to set on that particular survey
    * @return list Of succeeded and failed modifications according to internal validation.
    """
    def set_language_properties(self):
        return;
    """
    * RPC Routine to set survey language properties.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iSurveyID - ID of the survey
    * @param list|struct $aSurveyLocaleData - An list with the particular fieldnames as keys and their values to set on that particular survey
    * @param string $sLanguage - Optional - Language to update - if not give the base language of the particular survey is used
    * @return list Status=>OK, when save successful otherwise error text.
    """
    def set_participant_properties(self):
        return;
    """
    * RPC Routine to set properties of a survey participant/token.
    * Returns list
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the survey that participants belong
    * @param int $iTokenID Id of the participant to alter
    * @param list|struct $aTokenData Data to change
    * @return list Result of the change action
    """
    def set_question_properties(self):
        return;
    """
    * RPC Routine to set question properties.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iQuestionID - ID of the question
    * @param list|struct $aQuestionData - An list with the particular fieldnames as keys and their values to set on that particular question
    * @param string $sLanguage Optional parameter language for multilingual questions
    * @return list Of succeeded and failed modifications according to internal validation.
    """
    def set_survey_properties(self):
        return;
    """
    * RPC Routine to set survey properties.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param integer $iSurveyID - ID of the survey
    * @param list|struct $aSurveyData - An list with the particular fieldnames as keys and their values to set on that particular survey
    * @return list Of succeeded and failed nodifications according to internal validation.
    """
    def update_response(self):
        return;
    """
    * RPC Routine to update a response in a given survey.
    * Routine supports only single response updates.
    * Response to update will be identified either by the response id, or the token if response id is missing.
    * Routine is only applicable for active surveys with alloweditaftercompletion = Y.
    *
    * @access public
    * @param string $sSessionKey Auth credentials
    * @param int $iSurveyID Id of the Survey to update response
    * @param struct $aResponseData The actual response
    * @return mixed TRUE(bool) on success. errormessage on error
    """

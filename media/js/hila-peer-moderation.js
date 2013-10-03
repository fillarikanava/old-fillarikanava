/**
 * hila-peer-moderation.js
 *
 * Tools for voting and such.
 *
 * @author Joukkue HILA
 */
//<![CDATA[


comment_vote_json_source = "";
ratingUrl = "";
imageUrl = "";
allowed_to_vote = 0;

function prepareButtons ( rateUrl, voteUrl , mediaUrl, allowVote ) {
	ratingUrl = rateUrl;
	comment_vote_json_source = voteUrl;
	imageUrl = mediaUrl;
	allowed_to_Vote = allowVote;
}

function displayRatingData(requestUrl, voteUrl, allowVote) {
	
	$.ajax({
		url : requestUrl,
		dataType: 'json',
		success:  function(data) { 
		$.each(data, function(i, issue_data) {
			if (issue_data.issue_score != 'F')
			{	
				if (allowed_to_vote == 0) {
					buttonFor     (issue_data.issue_id, -1,  0 );
					buttonAgainst (issue_data.issue_id, -1,  0 );					
				}
				else if (issue_data.votecast > 0) {
					buttonFor     (issue_data.issue_id, -1,  0 );
					buttonAgainst (issue_data.issue_id, -1,  1 );
				}
				else  if (issue_data.votecast < 0) {
					buttonFor     (issue_data.issue_id, -1,  1 );
					buttonAgainst (issue_data.issue_id, -1,  0 );
				}
				else  {
					buttonFor     (issue_data.issue_id, -1,  1 );
					buttonAgainst (issue_data.issue_id, -1,  1 );
				}

				$( '#comment_-1_votesFor').html( issue_data.issue_votesfor);
				$( '#comment_-1_votesAgainst').html( issue_data.issue_votesagainst);

//				$( '#issue_' + issue_data.issue_id +'_score').html( issue_data.issue_score );
			}
			else
			{
				if (allowed_to_vote == 0) {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  0 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  0 );
				}
				else if (issue_data.votecast > 0) {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  0 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  1 );
				}
				else  if (issue_data.votecast < 0) {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  1 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  0 );
				}
				else  {
					buttonFor     (issue_data.issue_id, issue_data.comment_id,  1 );
					buttonAgainst (issue_data.issue_id, issue_data.comment_id,  1 );
				}

				$( '#comment_' + issue_data.comment_id +'_votesFor').html( issue_data.votesfor);
				$( '#comment_' + issue_data.comment_id +'_votesAgainst').html( issue_data.votesagainst);
			}
		})}})}



function loadCommentScores (json_url, issue_id, voteUrl) {
	displayRatingData (json_url + '?issue_id=' + issue_id, voteUrl);
}

function voteComment ( json_url, issue_id, message_id, value, voteUrl ) { 
	displayRatingData (json_url + '?issue_id=' + issue_id + '&message_id=' + message_id + '&score=' +value);
}


function buttonFor(issue_id, comment_id, activate) {
	if (activate == 1)
		$('#comment_' + comment_id +'_buttonFor').html('<a href="#"  onclick="voteComment(\'' + comment_vote_json_source + "', '" + issue_id + '\' , \'' +comment_id+ '\', \'1\' );"><img src="'+ imageUrl + 'images/thumb-up-active.png" alt="Up"></a>'); 
	else
		$('#comment_' + comment_id +'_buttonFor').html('<img src="'+ imageUrl + 'images/thumb-up-deactive.png" alt="Up">');
}

function buttonAgainst(issue_id, comment_id, activate) {
	if (activate == 1)
		$('#comment_' + comment_id +'_buttonAgainst').html('<a href="#"  onclick="voteComment(\'' + comment_vote_json_source + "', '" + issue_id + '\' , \'' +comment_id+ '\', \'-1\' );"><img src="'+ imageUrl + 'images/thumb-down-active.png" alt="Down"></a>'); 
	else
		$('#comment_' + comment_id +'_buttonAgainst').html('<img src="'+ imageUrl + 'images/thumb-down-deactive.png" alt="Down">');
}

//]]>
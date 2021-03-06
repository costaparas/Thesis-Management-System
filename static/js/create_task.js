function submitCreate() {
  const form = $('#create-task-form');
  if (!formValid(form)) {
    return;
  }

  $('#num-criteria').val($('[name^="marking-criteria-"]').length);

  $('#upload-spinner').toggle();
  $('#create-task-btn').toggle();
  makeMultiPartRequest('/create_task', form, (res) => {
    $('#upload-spinner').toggle();
    $('#create-task-btn').toggle();
    if (res.status === 'fail') {
      flash(res.message, error = true);
    } else {
      delayToast('Task created!', false);
      window.location.href = '/manage_courses';
    }
  });
}

function toggleSubmissionType() {
  if ($('#text-type').prop('checked') === true) {
    $('#text-entry-block').show();
    $('#file-size-block').hide();
    $('#file-type-block').hide();
  } else {
    $('#text-entry-block').hide();
    $('#file-size-block').show();
    $('#file-type-block').show();
  }
}

function toggleMarkingMethod() {
  if ($('#accept-method').prop('checked') === true) {
    $('#marking-criteria-block').hide();
  } else {
    $('#marking-criteria-block').show();
  }
}

$('[name="submission-type"]').change(function () {
  toggleSubmissionType();
});

$('[name="marking-method"]').change(function () {
  toggleMarkingMethod();
});

toggleSubmissionType();
toggleMarkingMethod();
$('#deadline').datetimepicker({
  'format': 'd/m/Y H:i',
  'lang': 'en'
});

function relabel(elem, attrs) {
  let id = 0;
  for (const attr of attrs) {
    val = elem.attr(attr);
    id = parseInt(val.match(/\d+$/)[0]);
    elem.attr(
      attr, val.replace(/(\d+)$/, function (all, n) {
        return parseInt(n) + 1;
      })
    );
  }
  return id + 1;
}

function addCriteria() {
  const lastCriteria = $('#criteria-table').find('[name^="marking-criteria-"]:last');
  const newCriteria = lastCriteria.clone();
  const id = relabel(newCriteria, ['id', 'name']);
  newCriteria.find('input').each(function () {
    relabel($(this), ['id', 'name']);
    $(this).val('');
    markFieldValid($(this));
  });
  newCriteria.find('[name="remove-criteria"]').attr('onclick', `removeCriteria(${id})`);
  newCriteria.insertAfter(lastCriteria);
  newCriteria.find('input:first').focus();
}

function removeCriteria(criteria) {
  const table = $('#criteria-table');
  if (table.find('tbody').find('tr').length > 2) {
    const toRemove = table.find(`#marking-criteria-${criteria}`);
    toRemove.remove();
  }
}

function removeOldAttachment() {
  $("#old-attachment-area").hide();
  const flag = $('#delete_old_attachment');
  flag.val('1');
}

$('#word-limit').on('input, change, keydown', function () {
  const val = $(this).val();
  if ($(this).hasClass('invalid')) {
    const max = parseInt($(this).attr('max'));
    if (val.match(/^\d+$/) && parseInt(val) > max) {
      $('#word-limit-error').attr('data-error', `Maximum word limit is ${max}`);
    } else if (!val.match(/^\d+$/)) {
      $('#word-limit-error').attr('data-error', 'Word limit is required');
    }
  }
});

$(document).ready(function(){
  $('.modal').modal();
});
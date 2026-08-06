frappe.ui.form.on("Employee", {
    refresh(frm) {
        const hide_button = setInterval(() => {
            $(".modal-dialog .modal-content .modal-footer .standard-actions .btn-modal-secondary").hide();
        }, 300);

        frm.__hide_button_interval = hide_button;
    },

    on_page_leave(frm) {
        if (frm.__hide_button_interval) {
            clearInterval(frm.__hide_button_interval);
        }
    }
});
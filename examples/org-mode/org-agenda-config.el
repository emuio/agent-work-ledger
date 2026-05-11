;;; org-agenda-config.el --- Minimal Agent Work Ledger org-agenda setup -*- lexical-binding: t; -*-

;; Add the projected agent agenda file to your agenda sources.
(add-to-list 'org-agenda-files "~/org/agent/agent-agenda.org")

;; Recommended TODO keywords for Agent Work Ledger states.
(setq org-todo-keywords
      '((sequence "INBOX(i)" "CLARIFYING(c)" "NEXT(n)" "RUNNING(r)" "WAITING(w)" "REVIEW(v)" "|" "DONE(d)" "CANCELLED(x)")))

;; Optional custom agenda commands.
(setq org-agenda-custom-commands
      '(("A" "Agent Work"
         ((tags-todo "agent"
                     ((org-agenda-overriding-header "Agent Work Ledger"))))
        ("R" "Agent Review Needed"
         ((todo "REVIEW"
                ((org-agenda-overriding-header "Agent tasks needing review")))))
        ("W" "Agent Waiting"
         ((todo "WAITING"
                ((org-agenda-overriding-header "Agent tasks waiting on people or systems")))))))

(provide 'org-agenda-config)

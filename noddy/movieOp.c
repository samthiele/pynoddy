/*
	This file was generated by XVT-Design 4.5, a product of:

		XVT Software Inc.
		4900 Pearl East Circle
		Boulder, CO USA 80301
		303-443-4223, fax 303-443-0969

	Generated on Tue Sep 02 10:34:59 1997
*/
/* TAG BEGIN SPCL:Pre_Header */
/* TAG END SPCL:Pre_Header */

#include "xvt.h"
#include "xvtcm.h"
#include "nodInc.h"

/* 
	Information about the window
*/
#define WIN_RES_ID MOVIE_OPTIONS
#define WIN_FLAGS 0x810L
#define WIN_CLASS ""
#define WIN_BORDER W_DOC
/* TAG BEGIN SPCL:Obj_Decl */
/* TAG END SPCL:Obj_Decl */

/*
	Handler for window MOVIE_OPTIONS ("Movie Options")
*/
long XVT_CALLCONV1
#if XVT_CC_PROTO
MOVIE_OPTIONS_eh XVT_CALLCONV2 (WINDOW xdWindow, EVENT *xdEvent)
#else
MOVIE_OPTIONS_eh XVT_CALLCONV2 (xdWindow, xdEvent)
WINDOW xdWindow;
EVENT *xdEvent;
#endif
{
	short xdControlId = xdEvent->v.ctl.id;
	/* TAG BEGIN SPCL:Var_Decl */
	/* TAG END SPCL:Var_Decl */

	switch (xdEvent->type) {
	case E_CREATE:
		/*
			Window has been created; first event sent to newly-created
			window.
		*/
		{
		/* TAG BEGIN EVNT:Create */
		int mmin, mmax;
			/* put this window in the created heirachy */
		addWinToStack (xdWindow);
							/* *************************** */
		mmin = 0; mmax = 30;		/* range for North East Corner */
		setScrollRange (xdWindow, MOVIE_SPEED_SCROLL, mmin, mmax);
		
					/* *********************************** */
					/* setup all the options in the window */
		loadGeologyMovieOptions (xdWindow);
		
				/* *************************************************** */
				/* Check the consistency of scrollbars and text fields */
		updateScrollAndText (xdWindow, MOVIE_SPEED_SCROLL, MOVIE_OPTIONS_SPEED, FALSE);
		/* TAG END EVNT:Create */
		}
		break;
	case E_DESTROY:
		/*
			Window has been closed; last event sent to window.
		*/
		xdRemoveHelpAssoc( xdWindow );
		{
		/* TAG BEGIN EVNT:Destroy */
			/* take this window out of the created heirachy */
		takeWinFromStack (xdWindow);
		/* TAG END EVNT:Destroy */
		}
		break;
	case E_FOCUS:
		{
		/* TAG BEGIN EVNT:Focus */
		/*
			Window has lost or gained focus.
		*/
		if (xdEvent->v.active) {
			/*
				Window has gained focus
			*/
		} else {
			/*
				Window has lost focus
			*/
		}
		/* TAG END EVNT:Focus */
		}
		break;
	case E_SIZE:
		/*
			Size of window has been set or changed; sent when window is
			created or subsequently resized by user or via xvt_vobj_move.
		*/
		{
		/* TAG BEGIN EVNT:Size */
		/* TAG END EVNT:Size */
		}
		break;
	case E_UPDATE:
		/*
			Window requires updating.
		*/
		{
		/* TAG BEGIN EVNT:Update */
		xvt_dwin_clear(xdWindow, (COLOR)xvt_vobj_get_attr(xdWindow, ATTR_BACK_COLOR));
		/* TAG END EVNT:Update */
		}
		break;
	case E_CLOSE:
		/*
			Request to close window; user operated "close" menu item on
			window system menu, or operated "close" control on window
			frame. Not sent if Close on File menu is issued. Window not
			closed unless xvt_vobj_destroy is called.
		*/
		{
		/* TAG BEGIN EVNT:Close */
		xvt_vobj_destroy(xdWindow);
		/* TAG END EVNT:Close */
		}
		break;
	case E_CHAR:
		/*
			Character typed.
		*/
		{
		/* TAG BEGIN EVNT:Char */
			/* *********************************************** */
			/* make a RETURN key activate the window OK Button */
		if (xdEvent->v.chr.ch == '\r')
		{
		   xdEvent->type = E_CONTROL;
		   xdEvent->v.ctl.id = MOVIE_OPTIONS_PUSHBUTTON_38;
		   xvt_win_dispatch_event (xdWindow, xdEvent);
		}
		/* TAG END EVNT:Char */
		}
		break;
	case E_MOUSE_UP:
		/*
			Mouse was released
		*/
		{
		/* TAG BEGIN EVNT:Mouse_Up */
		/* TAG END EVNT:Mouse_Up */
		}
		break;
	case E_MOUSE_DOWN:
		/*
			Mouse was pressed
		*/
		{
		/* TAG BEGIN EVNT:Mouse_Down */
		/* TAG END EVNT:Mouse_Down */
		}
		break;
	case E_MOUSE_DBL:
		/*
			Mouse was double clicked
		*/
		{
		/* TAG BEGIN EVNT:Mouse_Dbl */
		/* TAG END EVNT:Mouse_Dbl */
		}
		break;
	case E_MOUSE_MOVE:
		/*
			Mouse was moved
		*/
		{
		/* TAG BEGIN EVNT:Mouse_Move */
		/* TAG END EVNT:Mouse_Move */
		}
		break;
	case E_HSCROLL:
		{
		/* TAG BEGIN EVNT:Hscroll */
		/*
			Horizontal scrollbar on frame was operated
		*/
		switch (xdEvent->v.scroll.what) {
		case SC_LINE_UP:
			break;
		case SC_LINE_DOWN:
			break;
		case SC_PAGE_UP:
			break;
		case SC_PAGE_DOWN:
			break;
		case SC_THUMB:
			break;
		case SC_THUMBTRACK:
			break;
		default:
			break;
		}
		/* TAG END EVNT:Hscroll */
		}
		break;
	case E_VSCROLL:
		{
		/* TAG BEGIN EVNT:Vscroll */
		/*
			Vertical scrollbar on frame was operated
		*/
		switch (xdEvent->v.scroll.what) {
		case SC_LINE_UP:
			break;
		case SC_LINE_DOWN:
			break;
		case SC_PAGE_UP:
			break;
		case SC_PAGE_DOWN:
			break;
		case SC_THUMB:
			break;
		case SC_THUMBTRACK:
			break;
		default:
			break;
		}
		/* TAG END EVNT:Vscroll */
		}
		break;
	case E_COMMAND:
		/*
			User issued command on window menu bar (menu bar at top of
			screen for Mac/CH).
		*/
		{
		/* TAG BEGIN EVNT:Command */
		/*
			No menubar was associated with this window
		*/
		/* TAG END EVNT:Command */
		}
		break;
	case E_CONTROL:
		/*
			User operated control in window.
		*/
		{
		/* TAG BEGIN SPCL:Control_Decl */
		/* TAG END SPCL:Control_Decl */

		switch(xdControlId) {
		case MOVIE_OPTIONS_FRAMES: /* "frames" */
			{
			/* TAG BEGIN MOVIE_OPTIONS_FRAMES EVNT:Control */
			/*
				Edit control was operated.
			*/
			if (xdEvent->v.ctl.ci.v.edit.focus_change) {
				if (xdEvent->v.ctl.ci.v.edit.active) {
					/*
						focus has entered the control
					*/
				} else {
					/*
						focus has left the control
					*/
				}
			} else {
				/* 
					Contents of control were changed
				*/
			}
			/* TAG END MOVIE_OPTIONS_FRAMES EVNT:Control */
			}
			break;
		case MOVIE_SPEED_SCROLL: /* "Horizontal Scrollbar 4" */
			{
			/* TAG BEGIN MOVIE_SPEED_SCROLL EVNT:Control */
			int pos = 0;
			/*
				Horizontal scrollbar control was operated
			*/
			switch (xdEvent->v.ctl.ci.v.scroll.what) {
			case SC_LINE_UP:
				pos = xvt_sbar_get_pos (xdEvent->v.ctl.ci.win, HVSCROLL) - 1;
				break;
			case SC_LINE_DOWN:
				pos = xvt_sbar_get_pos (xdEvent->v.ctl.ci.win, HVSCROLL) + 1;
				break;
			case SC_PAGE_UP:
				pos = xvt_sbar_get_pos (xdEvent->v.ctl.ci.win, HVSCROLL) - TEN;
				SNAP_DOWN_BY(pos, 10)
				break;
			case SC_PAGE_DOWN:
				pos = xvt_sbar_get_pos (xdEvent->v.ctl.ci.win, HVSCROLL) + TEN;
				SNAP_UP_BY(pos, 10)
				break;
			case SC_THUMB:
				pos = xdEvent->v.ctl.ci.v.scroll.pos;
				break;
			case SC_THUMBTRACK:
				pos = xdEvent->v.ctl.ci.v.scroll.pos;
				break;
			}
			pos = updateScrollField (xdWindow, xdControlId, pos);
			updateNumericTextField (xdWindow, MOVIE_OPTIONS_SPEED, pos);
			/* TAG END MOVIE_SPEED_SCROLL EVNT:Control */
			}
			break;
		case MOVIE_OPTIONS_SPEED: /* "speed" */
			{
			/* TAG BEGIN MOVIE_OPTIONS_SPEED EVNT:Control */
			/*
				Edit control was operated.
			*/
			if (xdEvent->v.ctl.ci.v.edit.focus_change) {
				if (xdEvent->v.ctl.ci.v.edit.active) {
					/*
						focus has entered the control
					*/
				} else {
					/*
						focus has left the control
					*/
				}
			} else {
				/*
					Contents of control were changed
				*/
			updateScrollAndText (xdWindow, MOVIE_SPEED_SCROLL, MOVIE_OPTIONS_SPEED, FALSE);
			}
			/* TAG END MOVIE_OPTIONS_SPEED EVNT:Control */
			}
			break;
		case MOVIE_OPTIONS_PUSHBUTTON_38: /* "OK" */
			{
			/* TAG BEGIN MOVIE_OPTIONS_PUSHBUTTON_38 EVNT:Control */
						/* ********************************** */
						/* save all the options in the window */
			saveGeologyMovieOptions (xdWindow);
			xvt_vobj_destroy(xdWindow);
			/* TAG END MOVIE_OPTIONS_PUSHBUTTON_38 EVNT:Control */
			}
			break;
		case MOVIE_OPTIONS_PUSHBUTTON_39: /* "Cancel" */
			{
			/* TAG BEGIN MOVIE_OPTIONS_PUSHBUTTON_39 EVNT:Control */
			xvt_vobj_destroy(xdWindow);
			/* TAG END MOVIE_OPTIONS_PUSHBUTTON_39 EVNT:Control */
			}
			break;
		case MOVIE_OPTIONS_PUSHBUTTON_40: /* "Help..." */
			{
			/* TAG BEGIN MOVIE_OPTIONS_PUSHBUTTON_40 EVNT:Control */
			displayHelp("movieop.htm");
			/* TAG END MOVIE_OPTIONS_PUSHBUTTON_40 EVNT:Control */
			}
			break;
		case MOVIE_TYPE: /* "movietype" */
			{
			/* TAG BEGIN MOVIE_TYPE EVNT:Control */
			/* TAG END MOVIE_TYPE EVNT:Control */
			}
			break;
		default:
			break;
		}
		}
		break;
	case E_FONT:
		/*
			User issued font command on window menu bar (menu bar at top of
			screen for Mac/CH).
		*/
		{
		/* TAG BEGIN EVNT:Font */
		/* TAG END EVNT:Font */
		}
		break;
	case E_TIMER:
		/*
			Timer associated with window went off.
		*/
		{
		/* TAG BEGIN EVNT:Timer */
		/* TAG END EVNT:Timer */
		}
		break;
	case E_USER:
		/*
			Application initiated.
		*/
		{
		/* TAG BEGIN EVNT:User */
		switch (xdEvent->v.user.id) {
		case -1:
		default:
			break;
		}
		/* TAG END EVNT:User */
		}
		break;
	default:
		break;
	}
	/* TAG BEGIN SPCL:Bottom */
#ifdef XVT_R40_TXEDIT_BEHAVIOR
	xvt_tx_process_event(xdWindow, xdEvent);
#endif
	/* TAG END SPCL:Bottom */
	return 0L;
}
# Sippy B2BUA Notes

## General
* Uses a pool of UDP listeners/senders
* Event loop is run in the main thread; events must be scheduled onto the main thread
* UDP senders: multiplex over a queue to send packets out
* UDP listeners: use a callback to SipTransactionManager (STM)
* STM: new dialog forming request:
    * uses a callback from CallMap
* STM: new request:
    * UA object registers callback to handle in-dialog requests
* STM: response:
    * UA object registers callback to handle response
* ACK handling UAS:
    * the transaction state creates a "shadow" transaction that matches the incoming ACK
* ACK handling UAC:
    * ACKs are generated automatically and replayed (repeated 200 OK) by the STM core
	* 200 OK does not surface to the UA


## Call

A call is represented by CallController, this has an A-leg UA(uaA) and a B-leg UA(uaO).

uaA transitions through states `UasState*` (as UAS). 

uaO transitions through states `Uac*` (as UAC). In the connected state both are in the 
`UaStateConnected` state which handles BYE from either end.

Each UA handles actual SIP requests and responses on its side of the call.
The SIP states are signalled to the other leg using `CCEvent*` event.
Each leg is unaware of the other's SIP packets; the events contain SDP and metadata, sufficient
for a call leg to be created.

The clean separation of both legs, makes possible WebRTC bridging. If either UA is a WebRTC
agent we don't have to synthesise SIP messages. We need only create events for the other leg
to consume. 

## WebRTC Bridging

In the case of WebRTC, we create an agent, WS, that represents the WebRTC side of the call.
The WS agent, handles JSON signalling translating them to `CCEvent*`s; it also receives
events from the other leg, converting them to JSON .

The WS agent creates `CCEvent*`s with the same semantics as the SIP-to-SIP case; the other leg
is unaware that its partner is a UA or WS agent.

## UA Handling
* For each call, CallMap creates a CallController that has an A-leg UAS (uaA) and a B-leg
    UAC (uaO). To trigger pass-thru behaviour, each UA emits events in response to 
	INVITE, 200 OK, etc. The event is handled by the other leg's UA. I.e., the UAs do not see
	raw SIP messages from the other leg, but see events which are constructed based on SIP
	transactions
	
* INVITE: A-leg generates CCEventTry causing B-leg to send out INVITE
* 100 TRYING: B-leg generates CCEventRing
* 180 RINGING: B-leg generates CCEventRing
* 200 OK: B-leg geneates CCEventConnect
* ACK: this is handled independently by each leg. If A-leg does not receive ACK, a
    callback is triggered which disconnects the B-leg
* BYE: either leg generates CCEventDisconnect
* UAC: when creating transaction, will register a callback for the response
* UA: to handle in-dialog requests (e.g. BYE), the UA has registered a callback; both states
   `UacStateIdle` and `UasStateIdle` register a consumer based on Call-Id. The consumer
   in this case is the `recvRequest()` method of the UA object.

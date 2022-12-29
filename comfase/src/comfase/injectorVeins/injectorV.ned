

package comfase.comfase.injectorVeins;

simple injectorV
{
    parameters:
        @class(injectorV);

        double attackStartTime @unit("s");
        double attackEndTime @unit("s");
        bool attackOnSender ;// = default(false);
        bool attackOnReceiver ; //= default(false);
        
        bool delayAttack;
        double injectedPDValue @unit("s");
        bool DoSAttack;  
        double injectedPDforDoS @unit("s");
        bool destructiveInterferenceAttack;
        double injectedDestructiveness;    
        bool barrageJammingAttack;
        double injectedNoiseValue @unit("mW");  
        bool deceptiveJammingAttack;
        double injectedInterferenceValue @unit("mW");  
        
        string targetNodes;

}


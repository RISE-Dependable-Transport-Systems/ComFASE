
package comfase.comfase.injectorVeins;

simple injectorV
{
    parameters:
        @class(injectorV);

         // Mehdi
        double attackStartTime @unit("s");
        double attackEndTime @unit("s");
        double myPDValue @unit("s");
        double myPDforDoS @unit("s");
        bool attackActive ;// = default(false);
        bool attackOnSender ;// = default(false);
		bool attackOnReceiver ; //= default(false);
        int attackNode;
        bool DelayAttack;
        bool DoSAttack;  
        bool v_DelayAttack;
        bool uc2_DelayAttack;  
        double uc2_PDValue @unit("s");   
        bool SignalPowerAttack;
		bool ReceivePowerAttack;
        double myPowerValue @unit(mW);    
        double myR_PowerValue @unit(mW);  
        double myInterfValue @unit(mW);  
        bool InterferenceAttack;
        double myNoiseValue @unit(mW);  
        bool NoiseAttack;
        string myNodes;

}

